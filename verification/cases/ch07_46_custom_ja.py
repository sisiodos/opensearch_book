"""第7章 7.3.3: complete custom_ja book mapping and search synonyms

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import analyze, book_analysis, expect_ids, fragments, put, tokens

def run():
    i = book_analysis('customja', fragments(7)[0])
    put(i, 'a', {
        'description': 'パソコン',
    })
    put(i, 'b', {
        'description': 'PC',
    })
    expect_ids(i, {
        'match': {
            'description': 'PC',
        },
    }, ['a', 'b'])
    a = analyze({
        'analyzer': 'custom_ja',
        'text': 'PC',
    }, i)
    b = analyze({
        'analyzer': 'custom_ja_search',
        'text': 'PC',
    }, i)
    assert tokens(a) == ['pc'] and 'パソコン' in tokens(b)
    return {
        'index_tokens': a['tokens'],
        'search_tokens': b['tokens'],
    }
