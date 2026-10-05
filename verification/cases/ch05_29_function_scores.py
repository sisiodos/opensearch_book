"""第5章 5.9: log1p multiply yields zero for zero/missing count

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import fragments, score_fixture, search

def run():
    i = score_fixture()
    q = next((b['query'] for b in fragments(5) if 'function_score' in b.get('query', {})))
    r = search(i, q)
    scores = {h['_id']: h['_score'] for h in r['hits']['hits']}
    assert scores['zero'] == 0 and scores['missing'] == 0 and (scores['nine'] > 0)
    return scores
