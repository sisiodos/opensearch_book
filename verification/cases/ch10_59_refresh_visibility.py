"""第10章 10.1 / 10.4: refresh visibility and segment/flush APIs

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, req, search, total

def run():
    i = create('refresh', {
        'v': {
            'type': 'keyword',
        },
    }, settings={
        'refresh_interval': '-1',
    })
    req('PUT', f'/{i}/_doc/a', {
        'v': 'new',
    })
    assert req('GET', f'/{i}/_doc/a')['found']
    assert total(search(i)) == 0
    req('POST', f'/{i}/_refresh')
    assert total(search(i)) == 1
    req('POST', f'/{i}/_flush')
    return req('GET', f'/{i}/_segments')
