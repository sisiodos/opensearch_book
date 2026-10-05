"""第8章 8.4: distance sort and gauss decay at scale

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import fragments, geo_fixture, math, put, req, search

def run():
    i = geo_fixture('georank')
    b = fragments(8)
    sortbody = next((v for v in b if 'sort' in v))
    r = req('POST', f'/{i}/_search', sortbody)
    assert r['hits']['hits'][0]['_id'] == 'station'
    q = next((v['query'] for v in b if 'function_score' in v.get('query', {})))
    r = search(i, q)
    assert r['hits']['hits'][0]['_id'] == 'station'
    scores = {h['_id']: h['_score'] for h in r['hits']['hits']}
    assert math.isclose(scores['station'], 1, abs_tol=1e-05)
    put(i, 'scale', {
        'location': {
            'lat': 35.681236 + 1000 / 111195.08,
            'lon': 139.767125,
        },
    })
    r = search(i, q)
    score = next((h['_score'] for h in r['hits']['hits'] if h['_id'] == 'scale'))
    assert math.isclose(score, 0.5, abs_tol=0.003)
    return {
        'at_center': scores['station'],
        'approximately_1km': score,
    }
