"""第9章 9.3.2: title boost raises title match

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, fragments, put, search

def run():
    i = create('boost', {
        'title': {
            'type': 'text',
        },
        'body': {
            'type': 'text',
        },
    })
    put(i, 'title', {
        'title': 'OpenSearch',
        'body': 'other',
    })
    put(i, 'body', {
        'title': 'other',
        'body': 'OpenSearch',
    })
    q = next((v for v in fragments(9) if 'multi_match' in v))
    r = search(i, q)
    assert r['hits']['hits'][0]['_id'] == 'title'
    return {h['_id']: h['_score'] for h in r['hits']['hits']}
