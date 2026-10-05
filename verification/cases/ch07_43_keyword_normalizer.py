"""第7章 7.1.3: keyword rejects analyzer; normalizer retains one term

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import PREFIX, create, expect_ids, put, req

def run():
    r = req('PUT', '/' + PREFIX + 'badkw', {
        'mappings': {
            'properties': {
                'k': {
                    'type': 'keyword',
                    'analyzer': 'standard',
                },
            },
        },
    }, expected=(400,))
    i = create('norm', {
        'k': {
            'type': 'keyword',
            'normalizer': 'lower',
        },
    }, settings={
        'analysis': {
            'normalizer': {
                'lower': {
                    'type': 'custom',
                    'filter': ['lowercase'],
                },
            },
        },
    })
    put(i, 'a', {
        'k': 'OpenSearch Lucene',
    })
    expect_ids(i, {
        'term': {
            'k': 'OPENSEARCH LUCENE',
        },
    }, ['a'])
    return r['error']
