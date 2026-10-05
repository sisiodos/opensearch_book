"""第2章 2.1.5: boolean and keyword array containment

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import basic_fixture, expect_ids

def run():
    basic = basic_fixture()
    i = basic
    expect_ids(i, {
        'term': {
            'flag': True,
        },
    }, ['a'])
    expect_ids(i, {
        'term': {
            'tags': 'red',
        },
    }, ['a'])
