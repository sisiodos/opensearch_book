"""第2章 2.3.4: DocValues-only range, aggregate and sort

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, expect_ids, put

def run():
    i = create('dvonly', {
        'v': {
            'type': 'integer',
            'index': False,
        },
    })
    put(i, 'a', {
        'v': 2,
    })
    put(i, 'b', {
        'v': 8,
    })
    r = expect_ids(i, {
        'range': {
            'v': {
                'gte': 5,
            },
        },
    }, ['b'], sort=[{
        'v': 'desc',
    }], aggs={
        'avg': {
            'avg': {
                'field': 'v',
            },
        },
    })
    assert r['aggregations']['avg']['value'] == 8
