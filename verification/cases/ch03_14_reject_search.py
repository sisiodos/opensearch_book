"""第3章 3.4: text aggregation fails without fielddata

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import basic_fixture, reject_search

def run():
    basic = basic_fixture()
    return reject_search(basic, {
        'aggs': {
            'n': {
                'terms': {
                    'field': 'name',
                },
            },
        },
    })
