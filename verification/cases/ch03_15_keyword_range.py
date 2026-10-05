"""第3章 3.4: keyword lexicographic range differs from numeric

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, expect_ids, put

def run():
    i = create('lex', {
        's': {
            'type': 'keyword',
        },
        'n': {
            'type': 'integer',
        },
    })
    for v in (20, 100):
        put(i, str(v), {
            's': str(v),
            'n': v,
        })
    expect_ids(i, {
        'range': {
            's': {
                'lt': '20',
            },
        },
    }, ['100'])
    expect_ids(i, {
        'range': {
            'n': {
                'lt': 20,
            },
        },
    }, [])
