"""第2章 2.3.3: derived source reconstructs keyword array

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, put, req

def run():
    i = create('derived', {
        'tags': {
            'type': 'keyword',
        },
    }, settings={
        'index.derived_source.enabled': True,
    })
    put(i, 'a', {
        'tags': ['z', 'a', 'a'],
    })
    r = req('GET', f'/{i}/_doc/a')['_source']
    assert set(r['tags']) == {'a', 'z'}
    return {
        'input': ['z', 'a', 'a'],
        'reconstructed': r,
    }
