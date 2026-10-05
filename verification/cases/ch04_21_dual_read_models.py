"""第4章 4.3: product and SKU indexes from same source

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, put, search, total

def run():
    p = create('productmodel', {
        'product': {
            'type': 'keyword',
        },
        'skus': {
            'type': 'nested',
            'properties': {
                'sku': {
                    'type': 'keyword',
                },
            },
        },
    })
    k = create('skumodel', {
        'product': {
            'type': 'keyword',
        },
        'sku': {
            'type': 'keyword',
        },
    })
    put(p, 'p1', {
        'product': 'p1',
        'skus': [{
            'sku': 's1',
        }, {
            'sku': 's2',
        }],
    })
    for id in ('s1', 's2'):
        put(k, id, {
            'product': 'p1',
            'sku': id,
        })
    assert total(search(p)) == 1 and total(search(k)) == 2
    return {
        'products': 1,
        'skus': 2,
    }
