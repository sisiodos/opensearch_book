"""第6章 6.2.2: separate nested queries can match different elements

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import expect_ids, route

def run():
    i = route('nested', 'scope')
    q = {
        'bool': {
            'filter': [{
                'nested': {
                    'path': 'segments',
                    'query': {
                        'term': {
                            'segments.from': '東京',
                        },
                    },
                },
            }, {
                'nested': {
                    'path': 'segments',
                    'query': {
                        'term': {
                            'segments.to': '大阪',
                        },
                    },
                },
            }],
        },
    }
    expect_ids(i, q, ['route'])
