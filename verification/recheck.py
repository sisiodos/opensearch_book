import run as r
import json
from pathlib import Path
root=Path(__file__).resolve().parent
saved=json.loads((root/'results.json').read_text())
r.PREFIX=saved['prefix']+'recheck-'
r.exchanges=json.loads((root/'exchanges.json').read_text())
r.case(5,'5.2–5.7','book exact/prefix/match/phrase/range/terms/AND/sort examples',r.chapter5_search)
new=r.results[0]
assert new['status']=='PASS',new
saved['results']=[new if x['name']==new['name'] else x for x in saved['results']]
saved['indexes']+=r.indexes
(root/'results.json').write_text(json.dumps(saved,ensure_ascii=False,indent=2))
(root/'exchanges.json').write_text(json.dumps(r.exchanges,ensure_ascii=False,indent=2))
print('Final:',sum(x['status']=='PASS' for x in saved['results']),'PASS',sum(x['status']=='FAIL' for x in saved['results']),'FAIL')
