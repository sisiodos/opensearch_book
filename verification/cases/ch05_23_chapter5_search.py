"""第5章 5.2–5.7: book exact/prefix/match/phrase/range/terms/AND/sort examples

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import expect_ids, fragments, ids, json, product_fixture, search

def run():
    i = product_fixture()
    b = fragments(5)
    out = []
    for body in b:
        if 'query' not in body:
            continue
        q = body['query']
        txt = json.dumps(q, ensure_ascii=False)
        if any((t in txt for t in ('function_score', 'script_score', 'exists', 'stock.quantity', 'now-30d'))):
            continue
        r = search(i, q)
        out.append({
            'query': q,
            'ids': sorted(ids(r)),
        })
    expect_ids(i, {
        'term': {
            'product_id': 'ABC123',
        },
    }, ['ABC123'])
    expect_ids(i, {
        'prefix': {
            'product_name.keyword': 'ワイヤレス',
        },
    }, ['ABC123', 'C'])
    expect_ids(i, {
        'match': {
            'product_name': 'ワイヤレスイヤホン',
        },
    }, ['ABC123', 'B', 'C'])
    expect_ids(i, {
        'match_phrase': {
            'product_name': 'ワイヤレスイヤホン',
        },
    }, ['ABC123'])
    expect_ids(i, {
        'match': {
            'product_name': {
                'query': 'ワイヤレス イヤホン',
                'operator': 'and',
            },
        },
    }, ['ABC123'])
    expect_ids(i, {
        'range': {
            'price': {
                'gte': 1000,
                'lte': 5000,
            },
        },
    }, ['ABC123'])
    expect_ids(i, {
        'terms': {
            'category_code': ['ELEC', 'AUDIO', 'WEAR'],
        },
    }, ['ABC123', 'B', 'C'])
    r = search(i, sort=[{
        'price': 'asc',
    }, {
        'release_date': 'desc',
    }])
    assert [h['_id'] for h in r['hits']['hits']] == ['C', 'ABC123', 'B']
    return out
