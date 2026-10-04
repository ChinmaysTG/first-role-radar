"""First Role Radar: local job-research demo. No dependency installation required."""
import json, os, urllib.parse, urllib.request, http.server, pathlib
ROOT=pathlib.Path(__file__).parent
CACHE={}
# Optional local test cache, outside published source, avoids repeat credit use.
_cache_path=os.getenv("RADAR_TEST_CACHE")
if _cache_path:
    with open(_cache_path) as _cache_file: CACHE["junior software developer India"]=json.load(_cache_file)
REQUESTS_USED=0
MAX_LIVE_REQUESTS=int(os.getenv("RADAR_MAX_LIVE_REQUESTS","10"))
FIXTURE={"jobs_results":[{"title":"Junior Python Developer","company_name":"Demo company A","location":"Bengaluru, India","description":"Illustrative fixture only. Entry-level Python and SQL role, 0-1 years experience.","detected_extensions":{"schedule_type":"Full-time"},"apply_options":[]},{"title":"Software Engineering Intern","company_name":"Demo company B","location":"Remote, India","description":"Illustrative fixture only. Student internship using JavaScript.","detected_extensions":{"schedule_type":"Internship"},"apply_options":[]},{"title":"Senior Backend Engineer","company_name":"Demo company C","location":"Mumbai, India","description":"Illustrative fixture only. Requires 5+ years experience.","apply_options":[]}]}
def normalize(data):
    out=[]
    for item in data.get('jobs_results',[]):
        title=item.get('title',''); desc=item.get('description',''); text=(title+' '+desc).lower()
        beginner=any(word in text for word in ['junior','entry-level','intern','graduate','0-1']) and not any(word in title.lower() for word in ['senior','lead','principal'])
        links=[{'title':x.get('title','Apply'),'url':x['link']} for x in item.get('apply_options',[]) if x.get('link','').startswith('https://')]
        out.append({'title':title,'company':item.get('company_name','Not stated'),'location':item.get('location','Not stated'),'description':desc,'beginner_signal':beginner,'links':links,'salary':item.get('detected_extensions',{}).get('salary','Not stated')})
    return out
class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed=urllib.parse.urlparse(self.path)
        if parsed.path!='/api/jobs':
            self.path='/index.html' if parsed.path=='/' else parsed.path
            return super().do_GET()
        global REQUESTS_USED
        args=urllib.parse.parse_qs(parsed.query); query=args.get('q',['entry level developer India'])[0][:160]
        live=args.get('mode',['demo'])[0]=='live'; key=os.getenv('SERPAPI_API_KEY')
        try:
            if live:
                if not key: raise ValueError('Live mode needs SERPAPI_API_KEY on the local server. No search has been sent.')
                if query in CACHE: data=CACHE[query]
                else:
                    if REQUESTS_USED>=MAX_LIVE_REQUESTS: raise ValueError('Local search limit reached. No additional request sent.')
                    REQUESTS_USED+=1
                    url='https://serpapi.com/search?'+urllib.parse.urlencode({'engine':'google_jobs','q':query,'api_key':key})
                    try:
                        with urllib.request.urlopen(url,timeout=25) as res: data=json.load(res)
                    except Exception: raise ValueError('Search provider request failed. Check your secure key and provider quota locally.')
                    if data.get('error'): raise ValueError('Search provider rejected the request. Check your secure key and provider quota locally.')
                    CACHE[query]=data
            else: data=FIXTURE
            body=json.dumps({'mode':'live' if live else 'demo','jobs':normalize(data),'notice':'Live search results need checking on the employer page; no application is sent.' if live else 'Synthetic demo data, not real vacancies.'}).encode(); code=200
        except Exception as err:
            body=json.dumps({'error':str(err)}).encode(); code=400
        self.send_response(code); self.send_header('Content-Type','application/json'); self.send_header('Cache-Control','no-store'); self.end_headers(); self.wfile.write(body)
if __name__=='__main__':
    os.chdir(ROOT); http.server.HTTPServer(('127.0.0.1',8765),Handler).serve_forever()
