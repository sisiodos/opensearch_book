"""第5章 5.8: null_value distinguishes explicit null from missing

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, expect_ids, put, req

def run():
    i = create('nullvalue', {
        'price': {
            'type': 'float',
            'null_value': -1,
        },
    })
    for (id, d) in [('null', {
        'price': None,
    }), ('missing', {}), ('empty', {
        'price': [],
    }), ('zero', {
        'price': 0,
    })]:
        put(i, id, d)
    expect_ids(i, {
        'exists': {
            'field': 'price',
        },
    }, ['null', 'zero'])
    expect_ids(i, {
        'term': {
            'price': -1,
        },
    }, ['null'])
    assert req('GET', f'/{i}/_doc/null')['_source']['price'] is None
