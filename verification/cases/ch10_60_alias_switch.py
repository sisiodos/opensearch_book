"""第10章 10.3: replica setting and write alias switching

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import PREFIX, create, ids, put, req, search

def run():
    a = create('alias-a', {
        'v': {
            'type': 'keyword',
        },
    })
    b = create('alias-b', {
        'v': {
            'type': 'keyword',
        },
    })
    alias = PREFIX + 'write'
    req('POST', '/_aliases', {
        'actions': [{
            'add': {
                'index': a,
                'alias': alias,
                'is_write_index': True,
            },
        }],
    })
    put(alias, 'a', {
        'v': 'a',
    })
    req('POST', '/_aliases', {
        'actions': [{
            'remove': {
                'index': a,
                'alias': alias,
            },
        }, {
            'add': {
                'index': b,
                'alias': alias,
                'is_write_index': True,
            },
        }],
    })
    put(alias, 'b', {
        'v': 'b',
    })
    assert ids(search(a)) == {'a'} and ids(search(b)) == {'b'}
    req('PUT', f'/{b}/_settings', {
        'index': {
            'number_of_replicas': 1,
        },
    })
    health = req('GET', f'/_cluster/health/{b}')
    assert health['status'] == 'yellow'
    req('PUT', f'/{b}/_settings', {
        'index': {
            'number_of_replicas': 0,
        },
    })
    return {
        'single_node_with_one_replica': 'yellow',
        'alias_switch': 'pass',
    }
