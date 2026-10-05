"""第2章 2.2.1 / 2.2.5: numeric and parsed date range

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import basic_fixture, expect_ids

def run():
    basic = basic_fixture()
    i = basic
    expect_ids(i, {
        'range': {
            'price': {
                'gte': 50,
            },
        },
    }, ['a'])
    expect_ids(i, {
        'range': {
            'date': {
                'gte': '2024-05-02',
            },
        },
    }, ['b'])
