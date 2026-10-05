"""第2章 2.2.5: date_nanos retains fractional precision

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, put, search

def run():
    i = create('nanos', {
        'time': {
            'type': 'date_nanos',
        },
    })
    put(i, 'n', {
        'time': '2024-05-01T00:00:00.123456789Z',
    })
    r = search(i, fields=[{
        'field': 'time',
        'format': 'strict_date_optional_time_nanos',
    }], _source=False)
    assert r['hits']['hits'][0]['fields']['time'][0].endswith('123456789Z')
    return r['hits']['hits'][0]['fields']
