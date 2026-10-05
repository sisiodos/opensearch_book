"""HTTP操作、本文読み込み、共通の検証データ。"""
import json
import math
import os
import re
import time
import traceback
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from datetime import datetime, timezone, timedelta
BASE = 'http://127.0.0.1:19200'
ROOT = Path(__file__).resolve().parent
BOOK = Path(os.environ.get('BOOK_ROOT', str(ROOT.parent)))
PREFIX = 'lbv-' + uuid.uuid4().hex[:8] + '-'
results = []
exchanges = []
indexes = []
ROUTE = {
    'segments': [{
        'from': '東京',
        'to': '京都',
    }, {
        'from': '京都',
        'to': '大阪',
    }],
}

def req(method, path, body=None, expected=(200, 201)):
    data = None if body is None else json.dumps(body, ensure_ascii=False).encode()
    request = urllib.request.Request(BASE + path, data=data, method=method, headers={
        'Content-Type': 'application/json',
    })
    try:
        with urllib.request.urlopen(request, timeout=40) as r:
            status = r.status
            payload = json.load(r)
    except urllib.error.HTTPError as e:
        status = e.code
        payload = json.load(e)
    exchanges.append({
        'method': method,
        'path': path,
        'body': body,
        'status': status,
        'response': payload,
    })
    assert status in expected, (method, path, status, payload)
    return payload

def create(name, props=None, settings=None, extra=None):
    idx = PREFIX + name
    body = {
        'settings': {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        },
    }
    if settings:
        body['settings'].update(settings)
    if props is not None:
        body['mappings'] = {
            'properties': props,
        }
    if extra:
        body.update(extra)
    req('PUT', '/' + idx, body)
    indexes.append(idx)
    return idx

def put(idx, id, doc):
    return req('PUT', f'/{idx}/_doc/{id}?refresh=true', doc)

def search(idx, q=None, **kw):
    return req('POST', f'/{idx}/_search', {
        'size': 100,
        'query': q or {
            'match_all': {},
        },
        **kw,
    })

def ids(r):
    return {h['_id'] for h in r['hits']['hits']}

def total(r):
    return r['hits']['total']['value']

def expect_ids(idx, q, want, **kw):
    r = search(idx, q, **kw)
    assert ids(r) == set(want), (ids(r), want)
    return r

def case(ch, section, name, fn):
    n = len(exchanges)
    t = time.monotonic()
    try:
        evidence = fn()
        results.append({
            'chapter': ch,
            'section': section,
            'name': name,
            'status': 'PASS',
            'evidence': evidence,
            'exchanges': [n, len(exchanges)],
            'seconds': round(time.monotonic() - t, 3),
        })
    except Exception as e:
        results.append({
            'chapter': ch,
            'section': section,
            'name': name,
            'status': 'FAIL',
            'error': str(e),
            'traceback': traceback.format_exc(),
            'exchanges': [n, len(exchanges)],
        })
    print(f"{results[-1]['status']} ch{ch} {section} {name}", flush=True)

def fragments(ch):
    s = (BOOK / f'chapter{ch:02}.md').read_text()
    out = []
    for b in re.findall('```(?:json|http)\\n(.*?)\\n```', s, re.S):
        b = re.sub('^GET .*\\n', '', b)
        try:
            out.append(json.loads(b))
        except json.JSONDecodeError:
            out.append(json.loads('{' + b + '}'))
    return out

def reject_search(i, body):
    return req('POST', f'/{i}/_search', body, expected=(400,))['error']

def product_fixture():
    i = create('products', {
        'product_id': {
            'type': 'keyword',
        },
        'status': {
            'type': 'keyword',
        },
        'category_code': {
            'type': 'keyword',
        },
        'categories': {
            'type': 'keyword',
        },
        'product_name': {
            'type': 'text',
            'analyzer': 'ja',
            'fields': {
                'keyword': {
                    'type': 'keyword',
                },
            },
        },
        'price': {
            'type': 'integer',
        },
        'created_at': {
            'type': 'date',
        },
        'release_date': {
            'type': 'date',
        },
    }, settings={
        'analysis': {
            'analyzer': {
                'ja': {
                    'type': 'custom',
                    'tokenizer': 'book_ja',
                    'filter': ['lowercase'],
                },
            },
            'tokenizer': {
                'book_ja': {
                    'type': 'kuromoji_tokenizer',
                    'user_dictionary_rules': ['ワイヤレスイヤホン,ワイヤレス イヤホン,ワイヤレス イヤホン,カスタム名詞', 'ワイヤレススピーカー,ワイヤレス スピーカー,ワイヤレス スピーカー,カスタム名詞', 'イヤホン,イヤホン,イヤホン,カスタム名詞'],
                },
            },
        },
    })
    for (id, name, price, cat) in [('ABC123', 'ワイヤレスイヤホン', 2000, 'AUDIO'), ('B', 'イヤホン', 6000, 'AUDIO'), ('C', 'ワイヤレススピーカー', 500, 'ELEC')]:
        put(i, id, {
            'product_id': id,
            'status': 'available',
            'product_name': name,
            'price': price,
            'created_at': '2024-12-15',
            'release_date': '2024-12-15',
            'category_code': cat,
            'categories': ['アウトドア', '防水'] if id == 'ABC123' else ['アウトドア'],
        })
    return i

def score_fixture():
    i = create('scores', {
        'product_name': {
            'type': 'text',
        },
        'review_count': {
            'type': 'integer',
        },
        'rating': {
            'type': 'float',
        },
    })
    for (id, count) in [('zero', 0), ('nine', 9), ('missing', None)]:
        d = {
            'product_name': 'ワイヤレスイヤホン',
            'rating': 4,
        }
        if count is not None:
            d['review_count'] = count
        put(i, id, d)
    return i

def route(kind, name):
    i = create(name, {
        'segments': {
            'type': kind,
            'properties': {
                'from': {
                    'type': 'keyword',
                },
                'to': {
                    'type': 'keyword',
                },
            },
        },
    })
    put(i, 'route', ROUTE)
    return i

def pair(to):
    return {
        'bool': {
            'filter': [{
                'term': {
                    'segments.from': '東京',
                },
            }, {
                'term': {
                    'segments.to': to,
                },
            }],
        },
    }

def analyze(body, i=None):
    return req('POST', ('/' + i if i else '') + '/_analyze', body)

def tokens(r):
    return [t['token'] for t in r['tokens']]

def book_analysis(i, b):
    body = b.copy()
    body.setdefault('settings', {}).update({
        'number_of_shards': 1,
        'number_of_replicas': 0,
    })
    name = PREFIX + i
    req('PUT', '/' + name, body)
    indexes.append(name)
    return name

def geo_fixture(name):
    i = create(name, {
        'location': {
            'type': 'geo_point',
        },
    })
    for (id, lat, lon) in [('station', 35.681236, 139.767125), ('west', 35.6895, 139.72), ('far', 34.6937, 135.5023)]:
        put(i, id, {
            'location': {
                'lat': lat,
                'lon': lon,
            },
        })
    return i

def score_index(name, similarity='BM25', k1=1.2, b=0.75):
    i = create(name, {
        'title': {
            'type': 'text',
            'analyzer': 'whitespace',
            'similarity': 'book',
        },
        'body': {
            'type': 'text',
            'analyzer': 'whitespace',
            'similarity': 'book',
        },
        'popularity': {
            'type': 'float',
        },
    }, settings={
        'similarity': {
            'book': {
                'type': similarity,
                'k1': k1,
                'b': b,
            },
        },
    })
    for (id, t) in [('a', 'lucene lucene'), ('b', 'lucene extra extra extra'), ('c', 'other')]:
        put(i, id, {
            'title': t,
            'body': t,
            'popularity': 4,
        })
    return i

def basic_fixture():
    props = {
        'name': {
            'type': 'text',
        },
        'code': {
            'type': 'keyword',
        },
        'price': {
            'type': 'integer',
        },
        'date': {
            'type': 'date',
        },
        'flag': {
            'type': 'boolean',
        },
        'tags': {
            'type': 'keyword',
        },
        'display': {
            'type': 'keyword',
            'index': False,
            'doc_values': False,
        },
        'location': {
            'type': 'geo_point',
        },
    }
    basic = create('basic', props)
    put(basic, 'a', {
        'name': 'OpenSearch Lucene',
        'code': 'ABC123',
        'price': 100,
        'date': '2024-05-01',
        'flag': True,
        'tags': ['red', 'blue'],
        'display': 'original',
        'location': {
            'lat': 35.681236,
            'lon': 139.767125,
        },
    })
    put(basic, 'b', {
        'name': 'Lucene reference',
        'code': 'DEF456',
        'price': 20,
        'date': '2024-05-02',
        'flag': False,
        'tags': ['green'],
        'display': 'other',
        'location': {
            'lat': 35.7,
            'lon': 139.73,
        },
    })
    return basic
