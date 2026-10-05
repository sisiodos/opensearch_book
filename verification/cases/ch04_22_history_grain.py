"""第4章 4.5: history document count differs from people count

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, put, search, total

def run():
    i = create('history', {
        'user': {
            'type': 'keyword',
        },
        'score': {
            'type': 'integer',
        },
    })
    for (id, u) in [('h1', 'u1'), ('h2', 'u1'), ('h3', 'u2')]:
        put(i, id, {
            'user': u,
            'score': 86,
        })
    r = search(i, aggs={
        'people': {
            'cardinality': {
                'field': 'user',
            },
        },
    })
    assert total(r) == 3 and r['aggregations']['people']['value'] == 2
    return {
        'histories': 3,
        'people': 2,
    }
