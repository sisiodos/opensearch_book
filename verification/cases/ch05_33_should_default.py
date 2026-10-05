"""第5章 5.10: should optional only with must/filter by default

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, expect_ids, put

def run():
    i = create('should', {
        'tag': {
            'type': 'keyword',
        },
    })
    put(i, 'a', {
        'tag': 'yes',
    })
    put(i, 'b', {
        'tag': 'no',
    })
    expect_ids(i, {
        'bool': {
            'should': [{
                'term': {
                    'tag': 'yes',
                },
            }],
        },
    }, ['a'])
    expect_ids(i, {
        'bool': {
            'filter': {
                'match_all': {},
            },
            'should': [{
                'term': {
                    'tag': 'yes',
                },
            }],
        },
    }, ['a', 'b'])
