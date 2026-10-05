"""第5章 5.4: query format accepts dd/MM/yyyy

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, expect_ids, fragments, json, put

def run():
    i = create('format', {
        'created_at': {
            'type': 'date',
        },
    })
    put(i, 'a', {
        'created_at': '2024-12-15',
    })
    q = next((b['query'] for b in fragments(5) if 'dd/MM/yyyy' in json.dumps(b)))
    expect_ids(i, q, ['a'])
