"""第9章 9.3.3: sqrt(factor * popularity) multiply formula

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import fragments, math, put, score_index, search

def run():
    i = score_index('popularity')
    put(i, 'a', {
        'title': 'OpenSearch',
        'body': 'other',
        'popularity': 4,
    })
    q = next((v for v in fragments(9) if 'function_score' in v))
    base = search(i, {
        'match': {
            'title': 'OpenSearch',
        },
    })['hits']['hits'][0]['_score']
    got = search(i, q)['hits']['hits'][0]['_score']
    assert math.isclose(got, base * math.sqrt(1.5 * 4), rel_tol=1e-06)
    return {
        'actual': got,
        'expected': base * math.sqrt(6),
    }
