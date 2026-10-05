"""第1章 1.1: same _id replaces one document

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import basic_fixture, put, req

def run():
    basic = basic_fixture()
    i = basic
    d = req('GET', f'/{i}/_doc/a')['_source']
    put(i, 'a', d)
    assert req('GET', f'/{i}/_count')['count'] == 2
    return {
        'documents': 2,
        'id': 'a',
    }
