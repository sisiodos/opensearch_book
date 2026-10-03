import run as r,json
from pathlib import Path
root=Path(__file__).resolve().parent
saved=json.loads((root/'results.json').read_text());r.PREFIX=saved['prefix']+'extra-';r.exchanges=json.loads((root/'exchanges.json').read_text())
def caps():
 i=r.create('defaults',{'t':{'type':'text'},'k':{'type':'keyword'},'n':{'type':'long'},'b':{'type':'boolean'},'d':{'type':'date'},'g':{'type':'geo_point'}})
 c=r.req('GET',f'/{i}/_field_caps?fields=*')['fields']
 for f,typ in [('t','text'),('k','keyword'),('n','long'),('b','boolean'),('d','date'),('g','geo_point')]:assert c[f][typ]['searchable'] and c[f][typ]['aggregatable']==(f!='t')
 return {f:c[f] for f in ('t','k','n','b','d','g')}
def textkeyword():
 i=r.create('textkeyword',{'v':{'type':'text','analyzer':'keyword'}});r.put(i,'a',{'v':'OpenSearch Lucene'});assert r.tokens(r.analyze({'field':'v','text':'OpenSearch Lucene'},i))==['OpenSearch Lucene'];return r.reject_search(i,{'aggs':{'a':{'terms':{'field':'v'}}}})
def millis():
 i=r.create('millis',{'v':{'type':'date'}});r.put(i,'a',{'v':'2024-05-01T00:00:00.123456789Z'});out=r.search(i,fields=[{'field':'v','format':'strict_date_optional_time_nanos'}],_source=False)['hits']['hits'][0]['fields']['v'][0];assert out.endswith('.123Z');return out
def nestedagg():
 i=r.create('nestedagg',{'items':{'type':'nested','properties':{'v':{'type':'integer'}}}});r.put(i,'a',{'items':[{'v':1},{'v':2}]});o=r.search(i,aggs={'items':{'nested':{'path':'items'},'aggs':{'avg':{'avg':{'field':'items.v'}}}}})['aggregations']['items'];assert o['doc_count']==2 and o['avg']['value']==1.5;return o
r.case(3,'3.2','assert default field capabilities for all table types',caps)
r.case(7,'7.1.3','text with keyword analyzer remains text without aggregation',textkeyword)
r.case(5,'5.4','date format does not preserve nanosecond precision',millis)
r.case(6,'6.2.5','nested aggregation counts child scope',nestedagg)
assert all(x['status']=='PASS' for x in r.results),r.results
saved['results']+=r.results;saved['indexes']+=r.indexes
(root/'results.json').write_text(json.dumps(saved,ensure_ascii=False,indent=2));(root/'exchanges.json').write_text(json.dumps(r.exchanges,ensure_ascii=False,indent=2));print('Final',len(saved['results']),'PASS')
