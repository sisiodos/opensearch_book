"""第3章 3.2 / 3.3: geo_point sorting and aggregation

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import basic_fixture, search

def run():
    basic = basic_fixture()
    i = basic
    r = search(i, sort=[{
        '_geo_distance': {
            'location': {
                'lat': 35.681236,
                'lon': 139.767125,
            },
            'order': 'asc',
            'unit': 'km',
        },
    }], aggs={
        'bounds': {
            'geo_bounds': {
                'field': 'location',
            },
        },
    })
    assert r['hits']['hits'][0]['_id'] == 'a'
    return r['aggregations']
