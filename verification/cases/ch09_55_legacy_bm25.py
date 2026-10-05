"""第9章 9.2.2: LegacyBM25 scaling versus current BM25

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import math, score_index, search

def run():
    a = score_index('current')
    b = score_index('legacy', 'LegacyBM25')
    ra = search(a, {
        'match': {
            'title': 'lucene',
        },
    })
    rb = search(b, {
        'match': {
            'title': 'lucene',
        },
    })
    sa = {h['_id']: h['_score'] for h in ra['hits']['hits']}
    sb = {h['_id']: h['_score'] for h in rb['hits']['hits']}
    assert all((math.isclose(sb[k] / sa[k], 2.2, rel_tol=1e-06) for k in sa))
    return {
        'ratios': {k: sb[k] / sa[k] for k in sa},
    }
