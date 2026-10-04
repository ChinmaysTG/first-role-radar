import unittest
from server import normalize, FIXTURE
class Test(unittest.TestCase):
 def test_beginner(self): self.assertEqual([x['beginner_signal'] for x in normalize(FIXTURE)], [True,True,False])
 def test_unknown_salary(self): self.assertTrue(all(x['salary']=='Not stated' for x in normalize(FIXTURE)))
 def test_safe_links(self): self.assertEqual(normalize({'jobs_results':[{'apply_options':[{'link':'javascript:bad'},{'link':'https://employer.example/apply'}]}]})[0]['links'],[{'title':'Apply','url':'https://employer.example/apply'}])
 def test_empty(self): self.assertEqual(normalize({}), [])
 def test_salary_preserved(self): self.assertEqual(normalize({'jobs_results':[{'detected_extensions':{'salary':'₹20,000 a month'}}]})[0]['salary'],'₹20,000 a month')
 def test_senior_excluded(self): self.assertFalse(normalize({'jobs_results':[{'title':'Senior Engineer','description':'Mentor junior engineers'}]})[0]['beginner_signal'])
if __name__=='__main__': unittest.main()
