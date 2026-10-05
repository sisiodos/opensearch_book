"""第2章 2.1.1 / 2.1.4: term is raw; match analyzes text

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import basic_fixture, expect_ids

def run():
    basic = basic_fixture()
    i = basic
    expect_ids(i, {
        'term': {
            'name': 'Lucene',
        },
    }, [])
    expect_ids(i, {
        'match': {
            'name': 'Lucene',
        },
    }, ['a', 'b'])
    expect_ids(i, {
        'term': {
            'code': 'ABC',
        },
    }, [])
    expect_ids(i, {
        'term': {
            'code': 'ABC123',
        },
    }, ['a'])
