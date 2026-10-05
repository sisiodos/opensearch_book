"""第6章 6.1.1 / 6.2.2: object false positive vs nested same-element match

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import ROUTE, expect_ids, pair, req, route

def run():
    o = route('object', 'route-object')
    n = route('nested', 'route-nested')
    expect_ids(o, pair('大阪'), ['route'])
    expect_ids(n, {
        'nested': {
            'path': 'segments',
            'query': pair('大阪'),
        },
    }, [])
    expect_ids(n, {
        'nested': {
            'path': 'segments',
            'query': pair('京都'),
        },
    }, ['route'])
    assert req('GET', f'/{o}/_doc/route')['_source'] == ROUTE
