"""第3章 3.5: index false still validates numeric input

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, req

def run():
    i = create('validate', {
        'v': {
            'type': 'integer',
            'index': False,
            'doc_values': False,
        },
    })
    return req('PUT', f'/{i}/_doc/a', {
        'v': 'not-a-number',
    }, expected=(400,))['error']
