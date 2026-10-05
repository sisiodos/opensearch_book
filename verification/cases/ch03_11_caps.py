"""第3章 3.2: assert default field capabilities for all table types

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, req

def run():
    i = create('defaults', {
        't': {
            'type': 'text',
        },
        'k': {
            'type': 'keyword',
        },
        'n': {
            'type': 'long',
        },
        'b': {
            'type': 'boolean',
        },
        'd': {
            'type': 'date',
        },
        'g': {
            'type': 'geo_point',
        },
    })
    c = req('GET', f'/{i}/_field_caps?fields=*')['fields']
    for (f, typ) in [('t', 'text'), ('k', 'keyword'), ('n', 'long'), ('b', 'boolean'), ('d', 'date'), ('g', 'geo_point')]:
        assert c[f][typ]['searchable'] and c[f][typ]['aggregatable'] == (f != 't')
    return {f: c[f] for f in ('t', 'k', 'n', 'b', 'd', 'g')}
