"""第5章 5.4: rolling 30 days excludes future dates

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, datetime, expect_ids, fragments, json, put, timedelta, timezone

def run():
    i = create('rolling', {
        'created_at': {
            'type': 'date',
        },
    })
    now = datetime.now(timezone.utc)
    for (id, days) in [('recent', -5), ('old', -31), ('future', 1)]:
        put(i, id, {
            'created_at': (now + timedelta(days=days)).isoformat(),
        })
    q = next((b['query'] for b in fragments(5) if 'now-30d' in json.dumps(b)))
    expect_ids(i, q, ['recent'])
