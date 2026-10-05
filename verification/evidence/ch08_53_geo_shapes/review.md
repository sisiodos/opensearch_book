# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch08_53_geo_shapes: PASS

第8章 8.5 — point array and geo_shape line/polygon fields

### PUT /lbv-7e280f3b-geoshapes

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "point": {
        "type": "geo_point"
      },
      "shape": {
        "type": "geo_shape"
      }
    }
  }
}
```

応答: HTTP 200

```json
{
  "acknowledged": true,
  "shards_acknowledged": true,
  "index": "lbv-7e280f3b-geoshapes"
}
```

### PUT /lbv-7e280f3b-geoshapes/_doc/a?refresh=true

リクエスト:

```json
{
  "point": [
    {
      "lat": 35.68,
      "lon": 139.76
    },
    {
      "lat": 34.69,
      "lon": 135.5
    }
  ],
  "shape": {
    "type": "linestring",
    "coordinates": [
      [
        139.75,
        35.67
      ],
      [
        139.77,
        35.69
      ]
    ]
  }
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-geoshapes",
  "_id": "a",
  "_version": 1,
  "result": "created",
  "forced_refresh": true,
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 0,
  "_primary_term": 1
}
```

### POST /lbv-7e280f3b-geoshapes/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "geo_shape": {
      "shape": {
        "shape": {
          "type": "envelope",
          "coordinates": [
            [
              139.74,
              35.7
            ],
            [
              139.78,
              35.66
            ]
          ]
        },
        "relation": "intersects"
      }
    }
  }
}
```

応答: HTTP 200

```json
{
  "took": 1,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.0,
    "hits": [
      {
        "_index": "lbv-7e280f3b-geoshapes",
        "_id": "a",
        "_score": 0.0,
        "_source": {
          "point": [
            {
              "lat": 35.68,
              "lon": 139.76
            },
            {
              "lat": 34.69,
              "lon": 135.5
            }
          ],
          "shape": {
            "type": "linestring",
            "coordinates": [
              [
                139.75,
                35.67
              ],
              [
                139.77,
                35.69
              ]
            ]
          }
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-geoshapes/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "geo_distance": {
      "distance": "2km",
      "point": {
        "lat": 35.681236,
        "lon": 139.767125
      }
    }
  }
}
```

応答: HTTP 200

```json
{
  "took": 1,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "lbv-7e280f3b-geoshapes",
        "_id": "a",
        "_score": 1.0,
        "_source": {
          "point": [
            {
              "lat": 35.68,
              "lon": 139.76
            },
            {
              "lat": 34.69,
              "lon": 135.5
            }
          ],
          "shape": {
            "type": "linestring",
            "coordinates": [
              [
                139.75,
                35.67
              ],
              [
                139.77,
                35.69
              ]
            ]
          }
        }
      }
    ]
  }
}
```

判定時の補足:

```json
null
```
