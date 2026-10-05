"""第7章 7.4.5: faq_query multi-word synonym graph

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import analyze, book_analysis, expect_ids, fragments, put

def run():
    b = fragments(7)[3]
    b['mappings'] = {
        'properties': {
            'body': {
                'type': 'text',
                'analyzer': 'standard',
                'search_analyzer': 'faq_query',
            },
        },
    }
    i = book_analysis('faq', b)
    put(i, 'a', {
        'body': 'personal computer',
    })
    put(i, 'b', {
        'body': 'pc',
    })
    expect_ids(i, {
        'match': {
            'body': 'PC',
        },
    }, ['a', 'b'])
    return analyze({
        'analyzer': 'faq_query',
        'text': 'PC',
    }, i)['tokens']
