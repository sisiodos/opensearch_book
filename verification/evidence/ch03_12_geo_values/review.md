# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch03_12_geo_values: PASS

第3章 3.2 / 3.3 — geo_point sorting and aggregation

### POST /lbv-7e280f3b-basic/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "match_all": {}
  },
  "sort": [
    {
      "_geo_distance": {
        "location": {
          "lat": 35.681236,
          "lon": 139.767125
        },
        "order": "asc",
        "unit": "km"
      }
    }
  ],
  "aggs": {
    "bounds": {
      "geo_bounds": {
        "field": "location"
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
      "value": 2,
      "relation": "eq"
    },
    "max_score": null,
    "hits": [
      {
        "_index": "lbv-7e280f3b-basic",
        "_id": "a",
        "_score": null,
        "_source": {
          "name": "OpenSearch Lucene",
          "code": "ABC123",
          "price": 100,
          "date": "2024-05-01",
          "flag": true,
          "tags": [
            "red",
            "blue"
          ],
          "display": "original",
          "location": {
            "lat": 35.681236,
            "lon": 139.767125
          }
        },
        "sort": [
          0.0
        ]
      },
      {
        "_index": "lbv-7e280f3b-basic",
        "_id": "b",
        "_score": null,
        "_source": {
          "name": "Lucene reference",
          "code": "DEF456",
          "price": 20,
          "date": "2024-05-02",
          "flag": false,
          "tags": [
            "green"
          ],
          "display": "other",
          "location": {
            "lat": 35.7,
            "lon": 139.73
          }
        },
        "sort": [
          3.9489746244965165
        ]
      }
    ]
  },
  "aggregations": {
    "bounds": {
      "bounds": {
        "top_left": {
          "lat": 35.69999998435378,
          "lon": 139.72999999299645
        },
        "bottom_right": {
          "lat": 35.68123596254736,
          "lon": 139.76712495088577
        }
      }
    }
  }
}
```

判定時の補足:

```json
{
  "bounds": {
    "bounds": {
      "top_left": {
        "lat": 35.69999998435378,
        "lon": 139.72999999299645
      },
      "bottom_right": {
        "lat": 35.68123596254736,
        "lon": 139.76712495088577
      }
    }
  }
}
```
