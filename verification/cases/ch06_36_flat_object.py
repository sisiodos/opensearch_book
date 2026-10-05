"""第6章 6.1.3: flat_object keeps keys out of mapping and exact lookup

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, expect_ids, put, req

def run():
    i = create('flat', {
        'price': {
            'type': 'integer',
        },
        'attributes': {
            'type': 'flat_object',
        },
    })
    put(i, 'a', {
        'price': 100,
        'attributes': {
            'custom_001': 'red',
            'n': '100',
        },
    })
    put(i, 'b', {
        'price': 20,
        'attributes': {
            'custom_002': 'blue',
            'n': '20',
        },
    })
    mapping = req('GET', f'/{i}/_mapping')[i]['mappings']['properties']['attributes']
    assert mapping == {
        'type': 'flat_object',
    }
    expect_ids(i, {
        'term': {
            'attributes.custom_001': 'red',
        },
    }, ['a'])
    r = req('POST', f'/{i}/_search', {
        'aggs': {
            'a': {
                'terms': {
                    'field': 'attributes.custom_001',
                },
            },
        },
    }, expected=(200, 400))
    return {
        'mapping': mapping,
        'internal_aggregation_response': r,
    }
