"""第7章 7.1–7.2: standard analyzer vs tokenizer vs keyword

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import analyze, tokens

def run():
    a = tokens(analyze({
        'analyzer': 'standard',
        'text': 'OpenSearch Lucene',
    }))
    t = tokens(analyze({
        'tokenizer': 'standard',
        'text': 'OpenSearch Lucene',
    }))
    k = tokens(analyze({
        'analyzer': 'keyword',
        'text': 'OpenSearch Lucene',
    }))
    assert a == ['opensearch', 'lucene'] and t == ['OpenSearch', 'Lucene'] and (k == ['OpenSearch Lucene'])
    return {
        'standard_analyzer': a,
        'standard_tokenizer': t,
        'keyword': k,
    }
