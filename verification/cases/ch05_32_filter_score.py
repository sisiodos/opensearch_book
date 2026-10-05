"""第5章 5.10: filter does not add score

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, ids, put, search

def run():
    i = create('filter', {
        'title': {
            'type': 'text',
        },
        'available': {
            'type': 'boolean',
        },
    })
    put(i, 'a', {
        'title': 'lucene',
        'available': True,
    })
    put(i, 'b', {
        'title': 'lucene',
        'available': False,
    })
    a = search(i, {
        'match': {
            'title': 'lucene',
        },
    })
    base = {h['_id']: h['_score'] for h in a['hits']['hits']}
    b = search(i, {
        'bool': {
            'must': {
                'match': {
                    'title': 'lucene',
                },
            },
            'filter': {
                'term': {
                    'available': True,
                },
            },
        },
    })
    assert ids(b) == {'a'} and b['hits']['hits'][0]['_score'] == base['a']
