"""第9章 9.2.2: BM25 explain agrees with book formula

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import math, req, score_index

def run():
    i = score_index('bm25')
    r = req('GET', f'/{i}/_explain/a', {
        'query': {
            'match': {
                'title': 'lucene',
            },
        },
    })
    score = r['explanation']['value']
    expected = math.log(1 + (3 - 2 + 0.5) / (2 + 0.5)) * 2 / (2 + 1.2 * (0.25 + 0.75 * (2 / (7 / 3))))
    assert math.isclose(score, expected, rel_tol=1e-06)
    return {
        'actual': score,
        'book_formula': expected,
        'explanation': r['explanation'],
    }
