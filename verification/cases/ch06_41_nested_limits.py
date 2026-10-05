"""第6章 6.2.5: depth/nested_fields/nested_objects limits reject excess

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import PREFIX, create, req

def run():
    evidence = []
    for (setting, props, doc) in [('index.mapping.depth.limit', {
        'a': {
            'properties': {
                'b': {
                    'properties': {
                        'c': {
                            'type': 'keyword',
                        },
                    },
                },
            },
        },
    }, None), ('index.mapping.nested_fields.limit', {
        'a': {
            'type': 'nested',
        },
        'b': {
            'type': 'nested',
        },
    }, None)]:
        r = req('PUT', '/' + PREFIX + setting.split('.')[-2], {
            'settings': {
                setting: 1,
            },
            'mappings': {
                'properties': props,
            },
        }, expected=(400,))
        evidence.append(r['error'])
    i = create('objectlimit', {
        'items': {
            'type': 'nested',
        },
    }, settings={
        'index.mapping.nested_objects.limit': 1,
    })
    r = req('PUT', f'/{i}/_doc/a', {
        'items': [{
            'v': 1,
        }, {
            'v': 2,
        }],
    }, expected=(400,))
    evidence.append(r['error'])
    return evidence
