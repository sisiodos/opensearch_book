"""第6章 6.1.2: dynamic keys grow mapping; repeated values do not

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, put, req

def run():
    i = create('dynamic')
    put(i, 'a', {
        'attributes': {
            'custom_001': 'a',
        },
    })
    put(i, 'b', {
        'attributes': {
            'custom_001': 'b',
        },
    })
    a = req('GET', f'/{i}/_mapping')[i]['mappings']['properties']['attributes']['properties']
    assert len(a) == 1
    put(i, 'c', {
        'attributes': {
            'custom_002': 'c',
        },
    })
    b = req('GET', f'/{i}/_mapping')[i]['mappings']['properties']['attributes']['properties']
    assert len(b) == 2
