#!/usr/bin/env python3
"""Book behavior checks. Uses only fresh lbv-* indexes on a dedicated local endpoint."""
import json, math, re, time, uuid, traceback, urllib.request, urllib.error, os
from pathlib import Path
from datetime import datetime, timezone, timedelta
BASE='http://127.0.0.1:19200'
ROOT=Path(__file__).resolve().parent
BOOK=Path(os.environ.get('BOOK_ROOT',str(ROOT.parent)))
PREFIX='lbv-'+uuid.uuid4().hex[:8]+'-'
results=[]; exchanges=[]; indexes=[]
def req(method,path,body=None,expected=(200,201)):
 data=None if body is None else json.dumps(body,ensure_ascii=False).encode()
 request=urllib.request.Request(BASE+path,data=data,method=method,headers={'Content-Type':'application/json'})
 try:
  with urllib.request.urlopen(request,timeout=40) as r: status=r.status; payload=json.load(r)
 except urllib.error.HTTPError as e: status=e.code; payload=json.load(e)
 exchanges.append({'method':method,'path':path,'body':body,'status':status,'response':payload})
 assert status in expected,(method,path,status,payload)
 return payload

def create(name,props=None,settings=None,extra=None):
 idx=PREFIX+name
 body={'settings':{'number_of_shards':1,'number_of_replicas':0}}
 if settings:body['settings'].update(settings)
 if props is not None:body['mappings']={'properties':props}
 if extra:body.update(extra)
 req('PUT','/'+idx,body);indexes.append(idx);return idx

def put(idx,id,doc):return req('PUT',f'/{idx}/_doc/{id}?refresh=true',doc)
def search(idx,q=None,**kw):return req('POST',f'/{idx}/_search',{'size':100,'query':q or {'match_all':{}},**kw})
def ids(r):return {h['_id'] for h in r['hits']['hits']}
def total(r):return r['hits']['total']['value']
def expect_ids(idx,q,want,**kw):
 r=search(idx,q,**kw);assert ids(r)==set(want),(ids(r),want);return r

def case(ch,section,name,fn):
 n=len(exchanges);t=time.monotonic()
 try:
  evidence=fn();results.append({'chapter':ch,'section':section,'name':name,'status':'PASS','evidence':evidence,'exchanges':[n,len(exchanges)],'seconds':round(time.monotonic()-t,3)})
 except Exception as e:
  results.append({'chapter':ch,'section':section,'name':name,'status':'FAIL','error':str(e),'traceback':traceback.format_exc(),'exchanges':[n,len(exchanges)]})
 print(f"{results[-1]['status']} ch{ch} {section} {name}",flush=True)

def fragments(ch):
 s=(BOOK/f'chapter{ch:02}.md').read_text()
 out=[]
 for b in re.findall(r'```(?:json|http)\n(.*?)\n```',s,re.S):
  b=re.sub(r'^GET .*\n','',b)
  try:out.append(json.loads(b))
  except json.JSONDecodeError:out.append(json.loads('{'+b+'}'))
 return out

def main():
 info=req('GET','/');ROOT.joinpath('environment.json').write_text(json.dumps(info,ensure_ascii=False,indent=2))
 print('OpenSearch '+info['version']['number']+' / Lucene '+info['version']['lucene_version'],flush=True)
 props={'name':{'type':'text'},'code':{'type':'keyword'},'price':{'type':'integer'},'date':{'type':'date'},'flag':{'type':'boolean'},'tags':{'type':'keyword'},'display':{'type':'keyword','index':False,'doc_values':False},'location':{'type':'geo_point'}}
 basic=create('basic',props)
 put(basic,'a',{'name':'OpenSearch Lucene','code':'ABC123','price':100,'date':'2024-05-01','flag':True,'tags':['red','blue'],'display':'original','location':{'lat':35.681236,'lon':139.767125}})
 put(basic,'b',{'name':'Lucene reference','code':'DEF456','price':20,'date':'2024-05-02','flag':False,'tags':['green'],'display':'other','location':{'lat':35.7,'lon':139.73}})
 case(1,'1.1','same _id replaces one document',lambda:replace_id(basic))
 case(1,'1.2–1.3','filter then aggregation/sort and source retrieval',lambda:basic_values(basic))
 case(2,'2.1.1 / 2.1.4','term is raw; match analyzes text',lambda:term_match(basic))
 case(2,'2.1.5','boolean and keyword array containment',lambda:bool_array(basic))
 case(2,'2.2.1 / 2.2.5','numeric and parsed date range',lambda:ranges(basic))
 case(2,'2.2.5','date_nanos retains fractional precision',date_nanos)
 case(2,'2.3.4','DocValues-only range, aggregate and sort',dv_only)
 case(2,'2.3.4','skip_list mapping and range',skip_list)
 case(2,'2.3.3','derived source reconstructs keyword array',derived)
 case(3,'3.2–3.3','field capabilities by type',lambda:req('GET',f'/{basic}/_field_caps?fields=*'))
 case(3,'3.2','assert default field capabilities for all table types',caps)
 case(3,'3.2 / 3.3','geo_point sorting and aggregation',lambda:geo_values(basic))
 case(3,'3.2 / 3.4','text accepts but ignores doc_values true and false',text_dv)
 case(3,'3.4','text aggregation fails without fielddata',lambda:reject_search(basic,{'aggs':{'n':{'terms':{'field':'name'}}}}))
 case(3,'3.4','keyword lexicographic range differs from numeric',keyword_range)
 case(3,'3.4–3.5','index/doc_values four combinations',four_combinations)
 case(3,'3.3 / 3.5','enabled false retains arbitrary object',disabled_object)
 case(3,'3.5','index false still validates numeric input',numeric_validation)
 case(3,'3.6','source filtering and facets in one request',lambda:source_facets(basic))
 case(4,'4.2 / 4.3','SKU collapse changes hits but not aggregation grain',collapse)
 case(4,'4.3','product and SKU indexes from same source',dual_read_models)
 case(4,'4.5','history document count differs from people count',history_grain)
 case(5,'5.2–5.7','book exact/prefix/match/phrase/range/terms/AND/sort examples',chapter5_search)
 case(5,'5.4','rolling 30 days excludes future dates',rolling_dates)
 case(5,'5.4','query format accepts dd/MM/yyyy',date_format)
 case(5,'5.4','date format does not preserve nanosecond precision',millis)
 case(5,'5.8','exists/null/empty/ignore_above behavior',exists_matrix)
 case(5,'5.8','null_value distinguishes explicit null from missing',null_value)
 case(5,'5.9','log1p multiply yields zero for zero/missing count',function_scores)
 case(5,'5.9','script_score replaces lexical score',script_scores)
 case(5,'5.10','exists inventory vs quantity > 0',stock)
 case(5,'5.10','filter does not add score',filter_score)
 case(5,'5.10','should optional only with must/filter by default',should_default)
 case(6,'6.1.1 / 6.2.2','object false positive vs nested same-element match',object_nested)
 case(6,'6.1.2','dynamic keys grow mapping; repeated values do not',dynamic_keys)
 case(6,'6.1.3','flat_object keeps keys out of mapping and exact lookup',flat_object)
 case(6,'6.2.2','separate nested queries can match different elements',nested_scopes)
 case(6,'6.2.3','application scalar pair key exact match',scalar_pairs)
 case(6,'6.2.5','100 nested objects produce 101 Lucene documents',nested_count)
 case(6,'6.2.5','nested aggregation counts child scope',nestedagg)
 case(6,'6.2.5','depth/nested_fields/nested_objects limits reject excess',nested_limits)
 case(7,'7.1–7.2','standard analyzer vs tokenizer vs keyword',analysis_basics)
 case(7,'7.1.3','keyword rejects analyzer; normalizer retains one term',keyword_normalizer)
 case(7,'7.1.3','text with keyword analyzer remains text without aggregation',textkeyword)
 case(7,'7.2','kuromoji tokenizer on Japanese example',kuromoji)
 case(7,'7.3.3','complete custom_ja book mapping and search synonyms',custom_ja)
 case(7,'7.4.3','natural_search definition and explicit Japanese stopwords',natural_search)
 case(7,'7.4.5','faq_query multi-word synonym graph',faq_search)
 case(7,'7.4.1','term/match/phrase/prefix/wildcard/regexp differences',query_types)
 case(8,'8.2','three coordinate formats give same search results',geo_formats)
 case(8,'8.3','book distance, box and polygon queries on points',geo_queries)
 case(8,'8.4','distance sort and gauss decay at scale',geo_rank)
 case(8,'8.5','point array and geo_shape line/polygon fields',geo_shapes)
 case(9,'9.2.2','BM25 explain agrees with book formula',bm25_formula)
 case(9,'9.2.2','LegacyBM25 scaling versus current BM25',legacy_bm25)
 case(9,'9.3.2','title boost raises title match',title_boost)
 case(9,'9.3.3','sqrt(factor * popularity) multiply formula',popularity)
 case(9,'9.3.4','custom BM25 k1/b settings change score',custom_bm25)
 case(10,'10.1 / 10.4','refresh visibility and segment/flush APIs',refresh_visibility)
 case(10,'10.3','replica setting and write alias switching',alias_switch)
 ROOT.joinpath('results.json').write_text(json.dumps({'prefix':PREFIX,'environment':info,'results':results,'indexes':indexes},ensure_ascii=False,indent=2))
 ROOT.joinpath('exchanges.json').write_text(json.dumps(exchanges,ensure_ascii=False,indent=2))
 print(f"PASS={sum(r['status']=='PASS' for r in results)} FAIL={sum(r['status']=='FAIL' for r in results)}",flush=True)
 if any(r['status']=='FAIL' for r in results):raise SystemExit(1)

# Assertions compare behavior, not prose or timing.
def replace_id(i):
 d=req('GET',f'/{i}/_doc/a')['_source'];put(i,'a',d);assert req('GET',f'/{i}/_count')['count']==2;return {'documents':2,'id':'a'}
def basic_values(i):
 r=search(i,{'range':{'price':{'gte':50}}},sort=[{'price':'asc'}],aggs={'avg':{'avg':{'field':'price'}}});assert ids(r)=={'a'} and r['aggregations']['avg']['value']==100 and r['hits']['hits'][0]['_source']['display']=='original';return {'avg':100}
def term_match(i):
 expect_ids(i,{'term':{'name':'Lucene'}},[]);expect_ids(i,{'match':{'name':'Lucene'}},['a','b']);expect_ids(i,{'term':{'code':'ABC'}},[]);expect_ids(i,{'term':{'code':'ABC123'}},['a'])
def bool_array(i):expect_ids(i,{'term':{'flag':True}},['a']);expect_ids(i,{'term':{'tags':'red'}},['a'])
def ranges(i):expect_ids(i,{'range':{'price':{'gte':50}}},['a']);expect_ids(i,{'range':{'date':{'gte':'2024-05-02'}}},['b'])
def date_nanos():
 i=create('nanos',{'time':{'type':'date_nanos'}});put(i,'n',{'time':'2024-05-01T00:00:00.123456789Z'});r=search(i,fields=[{'field':'time','format':'strict_date_optional_time_nanos'}],_source=False);assert r['hits']['hits'][0]['fields']['time'][0].endswith('123456789Z');return r['hits']['hits'][0]['fields']
def dv_only():
 i=create('dvonly',{'v':{'type':'integer','index':False}});put(i,'a',{'v':2});put(i,'b',{'v':8});r=expect_ids(i,{'range':{'v':{'gte':5}}},['b'],sort=[{'v':'desc'}],aggs={'avg':{'avg':{'field':'v'}}});assert r['aggregations']['avg']['value']==8

def skip_list():
 i=create('skip',{'v':{'type':'long','index':False,'skip_list':True}});put(i,'a',{'v':8});expect_ids(i,{'range':{'v':{'gte':5}}},['a']);return req('GET',f'/{i}/_mapping')
def derived():
 i=create('derived',{'tags':{'type':'keyword'}},settings={'index.derived_source.enabled':True});put(i,'a',{'tags':['z','a','a']});r=req('GET',f'/{i}/_doc/a')['_source'];assert set(r['tags'])=={'a','z'};return {'input':['z','a','a'],'reconstructed':r}
def geo_values(i):
 r=search(i,sort=[{'_geo_distance':{'location':{'lat':35.681236,'lon':139.767125},'order':'asc','unit':'km'}}],aggs={'bounds':{'geo_bounds':{'field':'location'}}});assert r['hits']['hits'][0]['_id']=='a';return r['aggregations']
def text_dv():
 evidence=[]
 for value in (True,False):
  i=create('textdv'+str(value).lower(),{'t':{'type':'text','doc_values':value}});put(i,'a',{'t':'hello'})
  mapping=req('GET',f'/{i}/_mapping')[i]['mappings']['properties']['t'];caps=req('GET',f'/{i}/_field_caps?fields=t')['fields']['t']['text']
  assert 'doc_values' not in mapping and not caps['aggregatable']
  error=reject_search(i,{'aggs':{'t':{'terms':{'field':'t'}}}})
  evidence.append({'input_doc_values':value,'mapping':mapping,'caps':caps,'aggregation_error':error})
 return evidence

def reject_search(i,body):return req('POST',f'/{i}/_search',body,expected=(400,))['error']
def keyword_range():
 i=create('lex',{'s':{'type':'keyword'},'n':{'type':'integer'}})
 for v in (20,100):put(i,str(v),{'s':str(v),'n':v})
 expect_ids(i,{'range':{'s':{'lt':'20'}}},['100']);expect_ids(i,{'range':{'n':{'lt':20}}},[])
def four_combinations():
 i=create('combos',{f'v{a}{b}':{'type':'integer','index':bool(a),'doc_values':bool(b)} for a in (0,1) for b in (0,1)});put(i,'a',{f'v{a}{b}':5 for a in (0,1) for b in (0,1)})
 for f in ('v01','v10','v11'):expect_ids(i,{'term':{f:5}},['a'])
 reject_search(i,{'query':{'term':{'v00':5}}});r=search(i,aggs={'a':{'avg':{'field':'v01'}}});assert r['aggregations']['a']['value']==5;reject_search(i,{'aggs':{'a':{'avg':{'field':'v10'}}}})
def disabled_object():
 i=create('disabled',{'raw_payload':{'type':'object','enabled':False}});d={'raw_payload':{'deep':{'v':[1,'two',{'x':True}]}}};put(i,'a',d);assert req('GET',f'/{i}/_doc/a')['_source']==d;assert 'deep' not in req('GET',f'/{i}/_mapping')[i]['mappings']['properties']['raw_payload']
def numeric_validation():
 i=create('validate',{'v':{'type':'integer','index':False,'doc_values':False}});return req('PUT',f'/{i}/_doc/a',{'v':'not-a-number'},expected=(400,))['error']
def source_facets(i):
 r=search(i,_source=['name'],aggs={'tags':{'terms':{'field':'tags'}}});assert set(r['hits']['hits'][0]['_source'])=={'name'} and r['aggregations']['tags']['buckets']
def collapse():
 i=create('collapse',{'product':{'type':'keyword'},'sku':{'type':'keyword'}})
 for id,p in [('s1','p1'),('s2','p1'),('s3','p2')]:put(i,id,{'sku':id,'product':p})
 r=search(i,collapse={'field':'product'},aggs={'products':{'terms':{'field':'product'}}});assert len(r['hits']['hits'])==2 and total(r)==3;assert sum(b['doc_count'] for b in r['aggregations']['products']['buckets'])==3;return {'collapsed_hits':2,'total':3,'aggregation_docs':3}
def dual_read_models():
 p=create('productmodel',{'product':{'type':'keyword'},'skus':{'type':'nested','properties':{'sku':{'type':'keyword'}}}});k=create('skumodel',{'product':{'type':'keyword'},'sku':{'type':'keyword'}})
 put(p,'p1',{'product':'p1','skus':[{'sku':'s1'},{'sku':'s2'}]})
 for id in ('s1','s2'):put(k,id,{'product':'p1','sku':id})
 assert total(search(p))==1 and total(search(k))==2;return {'products':1,'skus':2}
def history_grain():
 i=create('history',{'user':{'type':'keyword'},'score':{'type':'integer'}})
 for id,u in [('h1','u1'),('h2','u1'),('h3','u2')]:put(i,id,{'user':u,'score':86})
 r=search(i,aggs={'people':{'cardinality':{'field':'user'}}});assert total(r)==3 and r['aggregations']['people']['value']==2;return {'histories':3,'people':2}
def product_fixture():
 i=create('products',{'product_id':{'type':'keyword'},'status':{'type':'keyword'},'category_code':{'type':'keyword'},'categories':{'type':'keyword'},'product_name':{'type':'text','analyzer':'ja','fields':{'keyword':{'type':'keyword'}}},'price':{'type':'integer'},'created_at':{'type':'date'},'release_date':{'type':'date'}},settings={'analysis':{'analyzer':{'ja':{'type':'custom','tokenizer':'book_ja','filter':['lowercase']}},'tokenizer':{'book_ja':{'type':'kuromoji_tokenizer','user_dictionary_rules':['ワイヤレスイヤホン,ワイヤレス イヤホン,ワイヤレス イヤホン,カスタム名詞','ワイヤレススピーカー,ワイヤレス スピーカー,ワイヤレス スピーカー,カスタム名詞','イヤホン,イヤホン,イヤホン,カスタム名詞']}}}})
 for id,name,price,cat in [('ABC123','ワイヤレスイヤホン',2000,'AUDIO'),('B','イヤホン',6000,'AUDIO'),('C','ワイヤレススピーカー',500,'ELEC')]:put(i,id,{'product_id':id,'status':'available','product_name':name,'price':price,'created_at':'2024-12-15','release_date':'2024-12-15','category_code':cat,'categories':['アウトドア','防水'] if id=='ABC123' else ['アウトドア']})
 return i

def chapter5_search():
 i=product_fixture();b=fragments(5);out=[]
 # Execute exact published query fragments against matching fixtures.
 for body in b:
  if 'query' not in body:continue
  q=body['query'];txt=json.dumps(q,ensure_ascii=False)
  if any(t in txt for t in ('function_score','script_score','exists','stock.quantity','now-30d')):continue
  r=search(i,q);out.append({'query':q,'ids':sorted(ids(r))})
 expect_ids(i,{'term':{'product_id':'ABC123'}},['ABC123'])
 expect_ids(i,{'prefix':{'product_name.keyword':'ワイヤレス'}},['ABC123','C'])
 expect_ids(i,{'match':{'product_name':'ワイヤレスイヤホン'}},['ABC123','B','C'])
 expect_ids(i,{'match_phrase':{'product_name':'ワイヤレスイヤホン'}},['ABC123'])
 expect_ids(i,{'match':{'product_name':{'query':'ワイヤレス イヤホン','operator':'and'}}},['ABC123'])
 expect_ids(i,{'range':{'price':{'gte':1000,'lte':5000}}},['ABC123'])
 expect_ids(i,{'terms':{'category_code':['ELEC','AUDIO','WEAR']}},['ABC123','B','C'])
 r=search(i,sort=[{'price':'asc'},{'release_date':'desc'}]);assert [h['_id'] for h in r['hits']['hits']]==['C','ABC123','B'];return out

def rolling_dates():
 i=create('rolling',{'created_at':{'type':'date'}});now=datetime.now(timezone.utc)
 for id,days in [('recent',-5),('old',-31),('future',1)]:put(i,id,{'created_at':(now+timedelta(days=days)).isoformat()})
 q=next(b['query'] for b in fragments(5) if 'now-30d' in json.dumps(b));expect_ids(i,q,['recent'])
def date_format():
 i=create('format',{'created_at':{'type':'date'}});put(i,'a',{'created_at':'2024-12-15'});q=next(b['query'] for b in fragments(5) if 'dd/MM/yyyy' in json.dumps(b));expect_ids(i,q,['a'])
def exists_matrix():
 i=create('exists',{'v':{'type':'keyword','ignore_above':5},'dv':{'type':'keyword','index':False}})
 docs={'null':{'v':None},'missing':{},'emptyarray':{'v':[]},'emptystr':{'v':''},'array':{'v':[None,'one']},'long':{'v':'too-long'},'dv':{'dv':'exists'}}
 for id,d in docs.items():put(i,id,d)
 expect_ids(i,{'exists':{'field':'v'}},['emptystr','array']);expect_ids(i,{'exists':{'field':'dv'}},['dv']);return {'source_null_not_same_as_not_exists':True}
def null_value():
 i=create('nullvalue',{'price':{'type':'float','null_value':-1}})
 for id,d in [('null',{'price':None}),('missing',{}),('empty',{'price':[]}),('zero',{'price':0})]:put(i,id,d)
 expect_ids(i,{'exists':{'field':'price'}},['null','zero']);expect_ids(i,{'term':{'price':-1}},['null']);assert req('GET',f'/{i}/_doc/null')['_source']['price'] is None

def score_fixture():
 i=create('scores',{'product_name':{'type':'text'},'review_count':{'type':'integer'},'rating':{'type':'float'}})
 for id,count in [('zero',0),('nine',9),('missing',None)]:
  d={'product_name':'ワイヤレスイヤホン','rating':4}
  if count is not None:d['review_count']=count
  put(i,id,d)
 return i

def function_scores():
 i=score_fixture();q=next(b['query'] for b in fragments(5) if 'function_score' in b.get('query',{}));r=search(i,q);scores={h['_id']:h['_score'] for h in r['hits']['hits']};assert scores['zero']==0 and scores['missing']==0 and scores['nine']>0;return scores

def script_scores():
 i=create('script',{'product_name':{'type':'text'},'review_count':{'type':'integer'},'rating':{'type':'float'}});put(i,'a',{'product_name':'ワイヤレスイヤホン','review_count':9,'rating':4})
 q=next(b['query'] for b in fragments(5) if 'script_score' in b.get('query',{}));r=search(i,q);got=r['hits']['hits'][0]['_score'];assert math.isclose(got,math.log(11)+4,rel_tol=1e-6);return {'actual':got,'formula':math.log(11)+4}
def stock():
 i=create('stock',{'stock':{'properties':{'quantity':{'type':'integer'}}}})
 for id,n in [('zero',0),('negative',-1),('positive',2),('missing',None)]:put(i,id,{} if n is None else {'stock':{'quantity':n}})
 expect_ids(i,{'exists':{'field':'stock.quantity'}},['zero','negative','positive']);expect_ids(i,{'range':{'stock.quantity':{'gt':0}}},['positive'])
def filter_score():
 i=create('filter',{'title':{'type':'text'},'available':{'type':'boolean'}});put(i,'a',{'title':'lucene','available':True});put(i,'b',{'title':'lucene','available':False})
 a=search(i,{'match':{'title':'lucene'}});base={h['_id']:h['_score'] for h in a['hits']['hits']};b=search(i,{'bool':{'must':{'match':{'title':'lucene'}},'filter':{'term':{'available':True}}}});assert ids(b)=={'a'} and b['hits']['hits'][0]['_score']==base['a']
def should_default():
 i=create('should',{'tag':{'type':'keyword'}});put(i,'a',{'tag':'yes'});put(i,'b',{'tag':'no'})
 expect_ids(i,{'bool':{'should':[{'term':{'tag':'yes'}}]}},['a']);expect_ids(i,{'bool':{'filter':{'match_all':{}},'should':[{'term':{'tag':'yes'}}]}},['a','b'])
ROUTE={'segments':[{'from':'東京','to':'京都'},{'from':'京都','to':'大阪'}]}
def route(kind,name):
 i=create(name,{'segments':{'type':kind,'properties':{'from':{'type':'keyword'},'to':{'type':'keyword'}}}});put(i,'route',ROUTE);return i

def pair(to):return {'bool':{'filter':[{'term':{'segments.from':'東京'}},{'term':{'segments.to':to}}]}}
def object_nested():
 o=route('object','route-object');n=route('nested','route-nested');expect_ids(o,pair('大阪'),['route']);expect_ids(n,{'nested':{'path':'segments','query':pair('大阪')}},[]);expect_ids(n,{'nested':{'path':'segments','query':pair('京都')}},['route']);assert req('GET',f'/{o}/_doc/route')['_source']==ROUTE

def dynamic_keys():
 i=create('dynamic');put(i,'a',{'attributes':{'custom_001':'a'}});put(i,'b',{'attributes':{'custom_001':'b'}});a=req('GET',f'/{i}/_mapping')[i]['mappings']['properties']['attributes']['properties'];assert len(a)==1;put(i,'c',{'attributes':{'custom_002':'c'}});b=req('GET',f'/{i}/_mapping')[i]['mappings']['properties']['attributes']['properties'];assert len(b)==2

def flat_object():
 i=create('flat',{'price':{'type':'integer'},'attributes':{'type':'flat_object'}});put(i,'a',{'price':100,'attributes':{'custom_001':'red','n':'100'}});put(i,'b',{'price':20,'attributes':{'custom_002':'blue','n':'20'}})
 mapping=req('GET',f'/{i}/_mapping')[i]['mappings']['properties']['attributes'];assert mapping=={'type':'flat_object'};expect_ids(i,{'term':{'attributes.custom_001':'red'}},['a']);r=req('POST',f'/{i}/_search',{'aggs':{'a':{'terms':{'field':'attributes.custom_001'}}}},expected=(200,400));return {'mapping':mapping,'internal_aggregation_response':r}
def nested_scopes():
 i=route('nested','scope');q={'bool':{'filter':[{'nested':{'path':'segments','query':{'term':{'segments.from':'東京'}}}},{'nested':{'path':'segments','query':{'term':{'segments.to':'大阪'}}}}]}};expect_ids(i,q,['route'])
def scalar_pairs():
 i=create('pairs',{'segment_keys':{'type':'keyword'}});put(i,'a',{'segment_keys':['東京-京都','京都-大阪']});expect_ids(i,{'term':{'segment_keys':'東京-京都'}},['a']);expect_ids(i,{'term':{'segment_keys':'東京-大阪'}},[])
def nested_count():
 i=create('nestedcount',{'items':{'type':'nested','properties':{'v':{'type':'integer'}}}});put(i,'a',{'items':[{'v':n} for n in range(100)]});req('POST',f'/{i}/_flush');r=req('GET',f'/{i}/_stats/docs');assert r['_all']['primaries']['docs']['count']==101 and total(search(i))==1;return {'lucene_documents':101,'search_documents':1}
def nested_limits():
 evidence=[]
 for setting,props,doc in [('index.mapping.depth.limit',{'a':{'properties':{'b':{'properties':{'c':{'type':'keyword'}}}}}},None),('index.mapping.nested_fields.limit',{'a':{'type':'nested'},'b':{'type':'nested'}},None)]:
  r=req('PUT','/'+PREFIX+setting.split('.')[-2],{'settings':{setting:1},'mappings':{'properties':props}},expected=(400,));evidence.append(r['error'])
 i=create('objectlimit',{'items':{'type':'nested'}},settings={'index.mapping.nested_objects.limit':1});r=req('PUT',f'/{i}/_doc/a',{'items':[{'v':1},{'v':2}]},expected=(400,));evidence.append(r['error']);return evidence

def analyze(body,i=None):return req('POST',(('/'+i) if i else '')+'/_analyze',body)
def tokens(r):return [t['token'] for t in r['tokens']]
def analysis_basics():
 a=tokens(analyze({'analyzer':'standard','text':'OpenSearch Lucene'}));t=tokens(analyze({'tokenizer':'standard','text':'OpenSearch Lucene'}));k=tokens(analyze({'analyzer':'keyword','text':'OpenSearch Lucene'}));assert a==['opensearch','lucene'] and t==['OpenSearch','Lucene'] and k==['OpenSearch Lucene'];return {'standard_analyzer':a,'standard_tokenizer':t,'keyword':k}
def keyword_normalizer():
 r=req('PUT','/'+PREFIX+'badkw',{'mappings':{'properties':{'k':{'type':'keyword','analyzer':'standard'}}}},expected=(400,))
 i=create('norm',{'k':{'type':'keyword','normalizer':'lower'}},settings={'analysis':{'normalizer':{'lower':{'type':'custom','filter':['lowercase']}}}});put(i,'a',{'k':'OpenSearch Lucene'});expect_ids(i,{'term':{'k':'OPENSEARCH LUCENE'}},['a']);return r['error']
def kuromoji():
 r=analyze({'tokenizer':'kuromoji_tokenizer','text':'私は学生です'});assert tokens(r)==['私','は','学生','です'];return r['tokens']
def book_analysis(i,b):
 body=b.copy();body.setdefault('settings',{}).update({'number_of_shards':1,'number_of_replicas':0});name=PREFIX+i;req('PUT','/'+name,body);indexes.append(name);return name

def custom_ja():
 i=book_analysis('customja',fragments(7)[0]);put(i,'a',{'description':'パソコン'});put(i,'b',{'description':'PC'});expect_ids(i,{'match':{'description':'PC'}},['a','b']);a=analyze({'analyzer':'custom_ja','text':'PC'},i);b=analyze({'analyzer':'custom_ja_search','text':'PC'},i);assert tokens(a)==['pc'] and 'パソコン' in tokens(b);return {'index_tokens':a['tokens'],'search_tokens':b['tokens']}
def natural_search():
 b=fragments(7)[1];b['mappings']={'properties':{'description':{'type':'text','analyzer':'custom_ja','search_analyzer':'natural_search'}}};b['settings']['analysis']['analyzer']['custom_ja']={'type':'custom','tokenizer':'kuromoji_tokenizer','filter':['kuromoji_baseform','kuromoji_part_of_speech','lowercase']};i=book_analysis('natural',b);put(i,'a',{'description':'安いパソコン'});expect_ids(i,{'match':{'description':'PC'}},['a']);r=analyze({'analyzer':'natural_search','text':'パソコンが安い'},i);assert 'が' not in tokens(r);return r['tokens']
def faq_search():
 b=fragments(7)[3];b['mappings']={'properties':{'body':{'type':'text','analyzer':'standard','search_analyzer':'faq_query'}}};i=book_analysis('faq',b);put(i,'a',{'body':'personal computer'});put(i,'b',{'body':'pc'});expect_ids(i,{'match':{'body':'PC'}},['a','b']);return analyze({'analyzer':'faq_query','text':'PC'},i)['tokens']
def query_types():
 i=create('types',{'t':{'type':'text'},'k':{'type':'keyword'}});put(i,'a',{'t':'OpenSearch Lucene','k':'OpenSearch Lucene'});put(i,'b',{'t':'Lucene OpenSearch','k':'Lucene OpenSearch'})
 expect_ids(i,{'term':{'t':'Lucene'}},[]);expect_ids(i,{'match':{'t':'Lucene'}},['a','b']);expect_ids(i,{'match_phrase':{'t':'OpenSearch Lucene'}},['a']);expect_ids(i,{'prefix':{'k':'Open'}},['a']);expect_ids(i,{'wildcard':{'k':'*Lucene'}},['a']);expect_ids(i,{'regexp':{'k':'Open.*'}},['a'])

def geo_fixture(name):
 i=create(name,{'location':{'type':'geo_point'}})
 for id,lat,lon in [('station',35.681236,139.767125),('west',35.6895,139.72),('far',34.6937,135.5023)]:put(i,id,{'location':{'lat':lat,'lon':lon}})
 return i

def geo_formats():
 i=create('geoformats',{'location':{'type':'geo_point'}})
 vals=['35.681236,139.767125',{'lat':35.681236,'lon':139.767125},[139.767125,35.681236]]
 for n,v in enumerate(vals):put(i,str(n),{'location':v})
 q=next(b['query'] for b in fragments(8) if 'geo_distance' in b.get('query',{}));expect_ids(i,q,['0','1','2'])
def geo_queries():
 i=geo_fixture('geoqueries');out=[]
 for b in fragments(8):
  q=b.get('query',{});kind=next(iter(q),'')
  if kind not in ('geo_distance','geo_bounding_box','geo_shape'):continue
  wanted=['west'] if kind=='geo_shape' else ['station'];r=expect_ids(i,q,wanted);out.append({'query_type':kind,'ids':sorted(ids(r))})
 return out

def geo_rank():
 i=geo_fixture('georank');b=fragments(8);sortbody=next(v for v in b if 'sort' in v);r=req('POST',f'/{i}/_search',sortbody);assert r['hits']['hits'][0]['_id']=='station';q=next(v['query'] for v in b if 'function_score' in v.get('query',{}));r=search(i,q);assert r['hits']['hits'][0]['_id']=='station';scores={h['_id']:h['_score'] for h in r['hits']['hits']};assert math.isclose(scores['station'],1,abs_tol=1e-5)
 # Near 1 km meridional offset; spherical approximation, not exact surveyed distance.
 put(i,'scale',{'location':{'lat':35.681236+1000/111195.08,'lon':139.767125}});r=search(i,q);score=next(h['_score'] for h in r['hits']['hits'] if h['_id']=='scale');assert math.isclose(score,0.5,abs_tol=0.003);return {'at_center':scores['station'],'approximately_1km':score}
def geo_shapes():
 i=create('geoshapes',{'point':{'type':'geo_point'},'shape':{'type':'geo_shape'}});put(i,'a',{'point':[{'lat':35.68,'lon':139.76},{'lat':34.69,'lon':135.5}],'shape':{'type':'linestring','coordinates':[[139.75,35.67],[139.77,35.69]]}})
 q={'geo_shape':{'shape':{'shape':{'type':'envelope','coordinates':[[139.74,35.7],[139.78,35.66]]},'relation':'intersects'}}};expect_ids(i,q,['a']);expect_ids(i,{'geo_distance':{'distance':'2km','point':{'lat':35.681236,'lon':139.767125}}},['a'])

def score_index(name,similarity='BM25',k1=1.2,b=0.75):
 i=create(name,{'title':{'type':'text','analyzer':'whitespace','similarity':'book'},'body':{'type':'text','analyzer':'whitespace','similarity':'book'},'popularity':{'type':'float'}},settings={'similarity':{'book':{'type':similarity,'k1':k1,'b':b}}})
 for id,t in [('a','lucene lucene'),('b','lucene extra extra extra'),('c','other')]:put(i,id,{'title':t,'body':t,'popularity':4})
 return i

def bm25_formula():
 i=score_index('bm25');r=req('GET',f'/{i}/_explain/a',{'query':{'match':{'title':'lucene'}}});score=r['explanation']['value'];expected=math.log(1+(3-2+0.5)/(2+0.5))*2/(2+1.2*(0.25+0.75*(2/(7/3))));assert math.isclose(score,expected,rel_tol=1e-6);return {'actual':score,'book_formula':expected,'explanation':r['explanation']}
def legacy_bm25():
 a=score_index('current');b=score_index('legacy','LegacyBM25');ra=search(a,{'match':{'title':'lucene'}});rb=search(b,{'match':{'title':'lucene'}});sa={h['_id']:h['_score'] for h in ra['hits']['hits']};sb={h['_id']:h['_score'] for h in rb['hits']['hits']};assert all(math.isclose(sb[k]/sa[k],2.2,rel_tol=1e-6) for k in sa);return {'ratios':{k:sb[k]/sa[k] for k in sa}}
def title_boost():
 i=create('boost',{'title':{'type':'text'},'body':{'type':'text'}});put(i,'title',{'title':'OpenSearch','body':'other'});put(i,'body',{'title':'other','body':'OpenSearch'});q=next(v for v in fragments(9) if 'multi_match' in v);r=search(i,q);assert r['hits']['hits'][0]['_id']=='title';return {h['_id']:h['_score'] for h in r['hits']['hits']}
def popularity():
 i=score_index('popularity');put(i,'a',{'title':'OpenSearch','body':'other','popularity':4});q=next(v for v in fragments(9) if 'function_score' in v);base=search(i,{'match':{'title':'OpenSearch'}})['hits']['hits'][0]['_score'];got=search(i,q)['hits']['hits'][0]['_score'];assert math.isclose(got,base*math.sqrt(1.5*4),rel_tol=1e-6);return {'actual':got,'expected':base*math.sqrt(6)}
def custom_bm25():
 a=score_index('bma');b=score_index('bmb',k1=2,b=0);sa=search(a,{'match':{'title':'lucene'}})['hits']['hits'][0]['_score'];sb=search(b,{'match':{'title':'lucene'}})['hits']['hits'][0]['_score'];assert sa!=sb;return {'default':sa,'custom':sb}
def refresh_visibility():
 i=create('refresh',{'v':{'type':'keyword'}},settings={'refresh_interval':'-1'});req('PUT',f'/{i}/_doc/a',{'v':'new'});assert req('GET',f'/{i}/_doc/a')['found'];assert total(search(i))==0;req('POST',f'/{i}/_refresh');assert total(search(i))==1;req('POST',f'/{i}/_flush');return req('GET',f'/{i}/_segments')
def alias_switch():
 a=create('alias-a',{'v':{'type':'keyword'}});b=create('alias-b',{'v':{'type':'keyword'}});alias=PREFIX+'write';req('POST','/_aliases',{'actions':[{'add':{'index':a,'alias':alias,'is_write_index':True}}]});put(alias,'a',{'v':'a'});req('POST','/_aliases',{'actions':[{'remove':{'index':a,'alias':alias}},{'add':{'index':b,'alias':alias,'is_write_index':True}}]});put(alias,'b',{'v':'b'});assert ids(search(a))=={'a'} and ids(search(b))=={'b'};req('PUT',f'/{b}/_settings',{'index':{'number_of_replicas':1}});health=req('GET',f'/_cluster/health/{b}');assert health['status']=='yellow';req('PUT',f'/{b}/_settings',{'index':{'number_of_replicas':0}});return {'single_node_with_one_replica':'yellow','alias_switch':'pass'}
def caps():
 i=create('defaults',{'t':{'type':'text'},'k':{'type':'keyword'},'n':{'type':'long'},'b':{'type':'boolean'},'d':{'type':'date'},'g':{'type':'geo_point'}})
 c=req('GET',f'/{i}/_field_caps?fields=*')['fields']
 for f,typ in [('t','text'),('k','keyword'),('n','long'),('b','boolean'),('d','date'),('g','geo_point')]:assert c[f][typ]['searchable'] and c[f][typ]['aggregatable']==(f!='t')
 return {f:c[f] for f in ('t','k','n','b','d','g')}
def textkeyword():
 i=create('textkeyword',{'v':{'type':'text','analyzer':'keyword'}});put(i,'a',{'v':'OpenSearch Lucene'});assert tokens(analyze({'field':'v','text':'OpenSearch Lucene'},i))==['OpenSearch Lucene'];return reject_search(i,{'aggs':{'a':{'terms':{'field':'v'}}}})
def millis():
 i=create('millis',{'v':{'type':'date'}});put(i,'a',{'v':'2024-05-01T00:00:00.123456789Z'});out=search(i,fields=[{'field':'v','format':'strict_date_optional_time_nanos'}],_source=False)['hits']['hits'][0]['fields']['v'][0];assert out.endswith('.123Z');return out
def nestedagg():
 i=create('nestedagg',{'items':{'type':'nested','properties':{'v':{'type':'integer'}}}});put(i,'a',{'items':[{'v':1},{'v':2}]});o=search(i,aggs={'items':{'nested':{'path':'items'},'aggs':{'avg':{'avg':{'field':'items.v'}}}}})['aggregations']['items'];assert o['doc_count']==2 and o['avg']['value']==1.5;return o

if __name__=='__main__':main()
