"""第9章 9.3.4: custom BM25 k1/b settings change score

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import score_index, search

def run():
    a = score_index('bma')
    b = score_index('bmb', k1=2, b=0)
    sa = search(a, {
        'match': {
            'title': 'lucene',
        },
    })['hits']['hits'][0]['_score']
    sb = search(b, {
        'match': {
            'title': 'lucene',
        },
    })['hits']['hits'][0]['_score']
    assert sa != sb
    return {
        'default': sa,
        'custom': sb,
    }
