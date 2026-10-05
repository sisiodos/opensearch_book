"""第7章 7.1.3: text with keyword analyzer remains text without aggregation

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import analyze, create, put, reject_search, tokens

def run():
    i = create('textkeyword', {
        'v': {
            'type': 'text',
            'analyzer': 'keyword',
        },
    })
    put(i, 'a', {
        'v': 'OpenSearch Lucene',
    })
    assert tokens(analyze({
        'field': 'v',
        'text': 'OpenSearch Lucene',
    }, i)) == ['OpenSearch Lucene']
    return reject_search(i, {
        'aggs': {
            'a': {
                'terms': {
                    'field': 'v',
                },
            },
        },
    })
