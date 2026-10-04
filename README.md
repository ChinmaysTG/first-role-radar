# First Role Radar
Student-focused job research using SerpApi Google Jobs. Original prototype for the SerpApi India Hackathon 2026.

## Run locally
Requires Python 3.9+ and a modern browser. No package installation needed.

```sh
python3 server.py
```
Open http://127.0.0.1:8765 . Synthetic mode uses clearly labelled illustrative jobs and makes no external API calls.

## Live searches
Set `SERPAPI_API_KEY` in the local server environment using a secure local secret store before starting the server. Never put it into the HTML, repository or screen recording. Select Live SerpApi Google Jobs in the interface. A valid provider account and quota are needed. No billing or payment method is managed by this app.

The app calls the `google_jobs` engine, normalizes `jobs_results`, preserves source descriptions and HTTPS `apply_options`, and marks junior/intern/entry-level text signals. Missing salaries are shown as Not stated. Keyword signals are not confirmed eligibility. Students must verify employer identity, requirements and fees, then apply themselves.

## Credit and privacy safeguards
At most ten live provider requests per server run. Repeated identical queries use an in-memory cache. No polling, automatic applications or third-party browser trackers. API key stays on the Python server; errors do not expose request URLs or secrets. Requests to SerpApi transmit the job-search query. Use no private applicant data in queries.

## Tests
```sh
python3 -m unittest -v
```
Six normalization tests cover beginner signals, senior exclusion, missing salary, supplied salary, empty results and safe application links. HTTP smoke tests checked synthetic responses and safe failure without a key. One real Google Jobs query succeeded on 4 October 2026 and returned ten jobs. Search results can go stale; the app does not certify vacancy status.

## Optional local test cache
`RADAR_TEST_CACHE` may point to a local provider response, outside the repository. It caches the fixed demo query to avoid repeated API-credit use. Do not publish raw provider responses or private fields. Results shown from cache must be described as a cached real response, not a fresh search.

## Limitations
A prototype, not a full employment service. No background worker, account storage, user login, automatic applications or claim of applicant suitability. Source data and employer pages keep their respective rights and terms. A working free-tier query does not promise continued provider availability.

## AI-assisted development
AI assistance was used for project design, Python/HTML/JavaScript implementation, documentation and tests. No claim of unaided development is made.
