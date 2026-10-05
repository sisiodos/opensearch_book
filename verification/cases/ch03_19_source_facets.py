"""第3章 3.6: source filtering and facets in one request

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import basic_fixture, search

def run():
    basic = basic_fixture()
    i = basic
    r = search(i, _source=['name'], aggs={
        'tags': {
            'terms': {
                'field': 'tags',
            },
        },
    })
    assert set(r['hits']['hits'][0]['_source']) == {'name'} and r['aggregations']['tags']['buckets']
