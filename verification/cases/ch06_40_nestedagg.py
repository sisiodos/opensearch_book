"""第6章 6.2.5: nested aggregation counts child scope

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, put, search

def run():
    i = create('nestedagg', {
        'items': {
            'type': 'nested',
            'properties': {
                'v': {
                    'type': 'integer',
                },
            },
        },
    })
    put(i, 'a', {
        'items': [{
            'v': 1,
        }, {
            'v': 2,
        }],
    })
    o = search(i, aggs={
        'items': {
            'nested': {
                'path': 'items',
            },
            'aggs': {
                'avg': {
                    'avg': {
                        'field': 'items.v',
                    },
                },
            },
        },
    })['aggregations']['items']
    assert o['doc_count'] == 2 and o['avg']['value'] == 1.5
    return o
