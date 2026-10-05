"""第5章 5.4: date format does not preserve nanosecond precision

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, put, search

def run():
    i = create('millis', {
        'v': {
            'type': 'date',
        },
    })
    put(i, 'a', {
        'v': '2024-05-01T00:00:00.123456789Z',
    })
    out = search(i, fields=[{
        'field': 'v',
        'format': 'strict_date_optional_time_nanos',
    }], _source=False)['hits']['hits'][0]['fields']['v'][0]
    assert out.endswith('.123Z')
    return out
