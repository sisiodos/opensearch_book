"""第3章 3.3 / 3.5: enabled false retains arbitrary object

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, put, req

def run():
    i = create('disabled', {
        'raw_payload': {
            'type': 'object',
            'enabled': False,
        },
    })
    d = {
        'raw_payload': {
            'deep': {
                'v': [1, 'two', {
                    'x': True,
                }],
            },
        },
    }
    put(i, 'a', d)
    assert req('GET', f'/{i}/_doc/a')['_source'] == d
    assert 'deep' not in req('GET', f'/{i}/_mapping')[i]['mappings']['properties']['raw_payload']
