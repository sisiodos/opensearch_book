# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch08_51_geo_queries: PASS

第8章 8.3 — book distance, box and polygon queries on points

### PUT /lbv-7e280f3b-geoqueries

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "location": {
        "type": "geo_point"
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
  "index": "lbv-7e280f3b-geoqueries"
}
```

### PUT /lbv-7e280f3b-geoqueries/_doc/station?refresh=true

リクエスト:

```json
{
  "location": {
    "lat": 35.681236,
    "lon": 139.767125
  }
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-geoqueries",
  "_id": "station",
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

### PUT /lbv-7e280f3b-geoqueries/_doc/west?refresh=true

リクエスト:

```json
{
  "location": {
    "lat": 35.6895,
    "lon": 139.72
  }
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-geoqueries",
  "_id": "west",
  "_version": 1,
  "result": "created",
  "forced_refresh": true,
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 1,
  "_primary_term": 1
}
```

### PUT /lbv-7e280f3b-geoqueries/_doc/far?refresh=true

リクエスト:

```json
{
  "location": {
    "lat": 34.6937,
    "lon": 135.5023
  }
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-geoqueries",
  "_id": "far",
  "_version": 1,
  "result": "created",
  "forced_refresh": true,
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 2,
  "_primary_term": 1
}
```

### POST /lbv-7e280f3b-geoqueries/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "geo_distance": {
      "distance": "2km",
      "location": {
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
  "took": 3,
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
        "_index": "lbv-7e280f3b-geoqueries",
        "_id": "station",
        "_score": 1.0,
        "_source": {
          "location": {
            "lat": 35.681236,
            "lon": 139.767125
          }
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-geoqueries/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "geo_bounding_box": {
      "location": {
        "top_left": {
          "lat": 35.7,
          "lon": 139.75
        },
        "bottom_right": {
          "lat": 35.68,
          "lon": 139.78
        }
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
        "_index": "lbv-7e280f3b-geoqueries",
        "_id": "station",
        "_score": 1.0,
        "_source": {
          "location": {
            "lat": 35.681236,
            "lon": 139.767125
          }
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-geoqueries/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "geo_shape": {
      "location": {
        "shape": {
          "type": "polygon",
          "coordinates": [
            [
              [
                139.6917,
                35.6895
              ],
              [
                139.7,
                35.67
              ],
              [
                139.75,
                35.68
              ],
              [
                139.73,
                35.7
              ],
              [
                139.6917,
                35.6895
              ]
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
  "took": 2,
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
        "_index": "lbv-7e280f3b-geoqueries",
        "_id": "west",
        "_score": 0.0,
        "_source": {
          "location": {
            "lat": 35.6895,
            "lon": 139.72
          }
        }
      }
    ]
  }
}
```

判定時の補足:

```json
[
  {
    "query_type": "geo_distance",
    "ids": [
      "station"
    ]
  },
  {
    "query_type": "geo_bounding_box",
    "ids": [
      "station"
    ]
  },
  {
    "query_type": "geo_shape",
    "ids": [
      "west"
    ]
  }
]
```
