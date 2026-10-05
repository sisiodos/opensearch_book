"""第5章 5.9: script_score replaces lexical score

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, fragments, math, put, search

def run():
    i = create('script', {
        'product_name': {
            'type': 'text',
        },
        'review_count': {
            'type': 'integer',
        },
        'rating': {
            'type': 'float',
        },
    })
    put(i, 'a', {
        'product_name': 'ワイヤレスイヤホン',
        'review_count': 9,
        'rating': 4,
    })
    q = next((b['query'] for b in fragments(5) if 'script_score' in b.get('query', {})))
    r = search(i, q)
    got = r['hits']['hits'][0]['_score']
    assert math.isclose(got, math.log(11) + 4, rel_tol=1e-06)
    return {
        'actual': got,
        'formula': math.log(11) + 4,
    }
