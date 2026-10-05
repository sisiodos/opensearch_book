"""第8章 8.5: point array and geo_shape line/polygon fields

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import create, expect_ids, put

def run():
    i = create('geoshapes', {
        'point': {
            'type': 'geo_point',
        },
        'shape': {
            'type': 'geo_shape',
        },
    })
    put(i, 'a', {
        'point': [{
            'lat': 35.68,
            'lon': 139.76,
        }, {
            'lat': 34.69,
            'lon': 135.5,
        }],
        'shape': {
            'type': 'linestring',
            'coordinates': [[139.75, 35.67], [139.77, 35.69]],
        },
    })
    q = {
        'geo_shape': {
            'shape': {
                'shape': {
                    'type': 'envelope',
                    'coordinates': [[139.74, 35.7], [139.78, 35.66]],
                },
                'relation': 'intersects',
            },
        },
    }
    expect_ids(i, q, ['a'])
    expect_ids(i, {
        'geo_distance': {
            'distance': '2km',
            'point': {
                'lat': 35.681236,
                'lon': 139.767125,
            },
        },
    }, ['a'])
