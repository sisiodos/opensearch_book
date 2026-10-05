"""第7章 7.4.1: term/match/phrase/prefix/wildcard/regexp differences

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, expect_ids, put

def run():
    i = create('types', {
        't': {
            'type': 'text',
        },
        'k': {
            'type': 'keyword',
        },
    })
    put(i, 'a', {
        't': 'OpenSearch Lucene',
        'k': 'OpenSearch Lucene',
    })
    put(i, 'b', {
        't': 'Lucene OpenSearch',
        'k': 'Lucene OpenSearch',
    })
    expect_ids(i, {
        'term': {
            't': 'Lucene',
        },
    }, [])
    expect_ids(i, {
        'match': {
            't': 'Lucene',
        },
    }, ['a', 'b'])
    expect_ids(i, {
        'match_phrase': {
            't': 'OpenSearch Lucene',
        },
    }, ['a'])
    expect_ids(i, {
        'prefix': {
            'k': 'Open',
        },
    }, ['a'])
    expect_ids(i, {
        'wildcard': {
            'k': '*Lucene',
        },
    }, ['a'])
    expect_ids(i, {
        'regexp': {
            'k': 'Open.*',
        },
    }, ['a'])
