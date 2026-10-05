"""第1章 1.2–1.3: filter then aggregation/sort and source retrieval

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import basic_fixture, ids, search

def run():
    basic = basic_fixture()
    i = basic
    r = search(i, {
        'range': {
            'price': {
                'gte': 50,
            },
        },
    }, sort=[{
        'price': 'asc',
    }], aggs={
        'avg': {
            'avg': {
                'field': 'price',
            },
        },
    })
    assert ids(r) == {'a'} and r['aggregations']['avg']['value'] == 100 and (r['hits']['hits'][0]['_source']['display'] == 'original')
    return {
        'avg': 100,
    }
