"""第7章 7.4.3: natural_search definition and explicit Japanese stopwords

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import analyze, book_analysis, expect_ids, fragments, put, tokens

def run():
    b = fragments(7)[1]
    b['mappings'] = {
        'properties': {
            'description': {
                'type': 'text',
                'analyzer': 'custom_ja',
                'search_analyzer': 'natural_search',
            },
        },
    }
    b['settings']['analysis']['analyzer']['custom_ja'] = {
        'type': 'custom',
        'tokenizer': 'kuromoji_tokenizer',
        'filter': ['kuromoji_baseform', 'kuromoji_part_of_speech', 'lowercase'],
    }
    i = book_analysis('natural', b)
    put(i, 'a', {
        'description': '安いパソコン',
    })
    expect_ids(i, {
        'match': {
            'description': 'PC',
        },
    }, ['a'])
    r = analyze({
        'analyzer': 'natural_search',
        'text': 'パソコンが安い',
    }, i)
    assert 'が' not in tokens(r)
    return r['tokens']
