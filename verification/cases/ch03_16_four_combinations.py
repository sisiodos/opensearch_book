"""第3章 3.4–3.5: index/doc_values four combinations

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, expect_ids, put, reject_search, search

def run():
    i = create('combos', {f'v{a}{b}': {
        'type': 'integer',
        'index': bool(a),
        'doc_values': bool(b),
    } for a in (0, 1) for b in (0, 1)})
    put(i, 'a', {f'v{a}{b}': 5 for a in (0, 1) for b in (0, 1)})
    for f in ('v01', 'v10', 'v11'):
        expect_ids(i, {
            'term': {
                f: 5,
            },
        }, ['a'])
    reject_search(i, {
        'query': {
            'term': {
                'v00': 5,
            },
        },
    })
    r = search(i, aggs={
        'a': {
            'avg': {
                'field': 'v01',
            },
        },
    })
    assert r['aggregations']['a']['value'] == 5
    reject_search(i, {
        'aggs': {
            'a': {
                'avg': {
                    'field': 'v10',
                },
            },
        },
    })
