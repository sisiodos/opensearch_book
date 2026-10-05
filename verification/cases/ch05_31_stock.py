"""第5章 5.10: exists inventory vs quantity > 0

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, expect_ids, put

def run():
    i = create('stock', {
        'stock': {
            'properties': {
                'quantity': {
                    'type': 'integer',
                },
            },
        },
    })
    for (id, n) in [('zero', 0), ('negative', -1), ('positive', 2), ('missing', None)]:
        put(i, id, {} if n is None else {
            'stock': {
                'quantity': n,
            },
        })
    expect_ids(i, {
        'exists': {
            'field': 'stock.quantity',
        },
    }, ['zero', 'negative', 'positive'])
    expect_ids(i, {
        'range': {
            'stock.quantity': {
                'gt': 0,
            },
        },
    }, ['positive'])
