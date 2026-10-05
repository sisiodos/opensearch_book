"""第5章 5.8: exists/null/empty/ignore_above behavior

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, expect_ids, put

def run():
    i = create('exists', {
        'v': {
            'type': 'keyword',
            'ignore_above': 5,
        },
        'dv': {
            'type': 'keyword',
            'index': False,
        },
    })
    docs = {
        'null': {
            'v': None,
        },
        'missing': {},
        'emptyarray': {
            'v': [],
        },
        'emptystr': {
            'v': '',
        },
        'array': {
            'v': [None, 'one'],
        },
        'long': {
            'v': 'too-long',
        },
        'dv': {
            'dv': 'exists',
        },
    }
    for (id, d) in docs.items():
        put(i, id, d)
    expect_ids(i, {
        'exists': {
            'field': 'v',
        },
    }, ['emptystr', 'array'])
    expect_ids(i, {
        'exists': {
            'field': 'dv',
        },
    }, ['dv'])
    return {
        'source_null_not_same_as_not_exists': True,
    }
