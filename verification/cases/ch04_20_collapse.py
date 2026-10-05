"""第4章 4.2 / 4.3: SKU collapse changes hits but not aggregation grain

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, put, search, total

def run():
    i = create('collapse', {
        'product': {
            'type': 'keyword',
        },
        'sku': {
            'type': 'keyword',
        },
    })
    for (id, p) in [('s1', 'p1'), ('s2', 'p1'), ('s3', 'p2')]:
        put(i, id, {
            'sku': id,
            'product': p,
        })
    r = search(i, collapse={
        'field': 'product',
    }, aggs={
        'products': {
            'terms': {
                'field': 'product',
            },
        },
    })
    assert len(r['hits']['hits']) == 2 and total(r) == 3
    assert sum((b['doc_count'] for b in r['aggregations']['products']['buckets'])) == 3
    return {
        'collapsed_hits': 2,
        'total': 3,
        'aggregation_docs': 3,
    }
