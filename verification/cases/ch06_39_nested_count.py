"""第6章 6.2.5: 100 nested objects produce 101 Lucene documents

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, put, req, search, total

def run():
    i = create('nestedcount', {
        'items': {
            'type': 'nested',
            'properties': {
                'v': {
                    'type': 'integer',
                },
            },
        },
    })
    put(i, 'a', {
        'items': [{
            'v': n,
        } for n in range(100)],
    })
    req('POST', f'/{i}/_flush')
    r = req('GET', f'/{i}/_stats/docs')
    assert r['_all']['primaries']['docs']['count'] == 101 and total(search(i)) == 1
    return {
        'lucene_documents': 101,
        'search_documents': 1,
    }
