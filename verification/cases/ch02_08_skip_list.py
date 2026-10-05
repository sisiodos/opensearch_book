"""第2章 2.3.4: skip_list mapping and range

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, expect_ids, put, req

def run():
    i = create('skip', {
        'v': {
            'type': 'long',
            'index': False,
            'skip_list': True,
        },
    })
    put(i, 'a', {
        'v': 8,
    })
    expect_ids(i, {
        'range': {
            'v': {
                'gte': 5,
            },
        },
    }, ['a'])
    return req('GET', f'/{i}/_mapping')
