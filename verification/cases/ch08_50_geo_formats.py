"""第8章 8.2: three coordinate formats give same search results

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, expect_ids, fragments, put

def run():
    i = create('geoformats', {
        'location': {
            'type': 'geo_point',
        },
    })
    vals = ['35.681236,139.767125', {
        'lat': 35.681236,
        'lon': 139.767125,
    }, [139.767125, 35.681236]]
    for (n, v) in enumerate(vals):
        put(i, str(n), {
            'location': v,
        })
    q = next((b['query'] for b in fragments(8) if 'geo_distance' in b.get('query', {})))
    expect_ids(i, q, ['0', '1', '2'])
