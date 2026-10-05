"""第3章 3.2 / 3.4: text accepts but ignores doc_values true and false

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, put, reject_search, req

def run():
    evidence = []
    for value in (True, False):
        i = create('textdv' + str(value).lower(), {
            't': {
                'type': 'text',
                'doc_values': value,
            },
        })
        put(i, 'a', {
            't': 'hello',
        })
        mapping = req('GET', f'/{i}/_mapping')[i]['mappings']['properties']['t']
        caps = req('GET', f'/{i}/_field_caps?fields=t')['fields']['t']['text']
        assert 'doc_values' not in mapping and (not caps['aggregatable'])
        error = reject_search(i, {
            'aggs': {
                't': {
                    'terms': {
                        'field': 't',
                    },
                },
            },
        })
        evidence.append({
            'input_doc_values': value,
            'mapping': mapping,
            'caps': caps,
            'aggregation_error': error,
        })
    return evidence
