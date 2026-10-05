"""第6章 6.2.3: application scalar pair key exact match

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, expect_ids, put

def run():
    i = create('pairs', {
        'segment_keys': {
            'type': 'keyword',
        },
    })
    put(i, 'a', {
        'segment_keys': ['東京-京都', '京都-大阪'],
    })
    expect_ids(i, {
        'term': {
            'segment_keys': '東京-京都',
        },
    }, ['a'])
    expect_ids(i, {
        'term': {
            'segment_keys': '東京-大阪',
        },
    }, [])
