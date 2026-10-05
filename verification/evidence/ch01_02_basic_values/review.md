# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch01_02_basic_values: PASS

第1章 1.2–1.3 — filter then aggregation/sort and source retrieval

### POST /lbv-7e280f3b-basic/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "range": {
      "price": {
        "gte": 50
      }
    }
  },
  "sort": [
    {
      "price": "asc"
    }
  ],
  "aggs": {
    "avg": {
      "avg": {
        "field": "price"
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
          100
        ]
      }
    ]
  },
  "aggregations": {
    "avg": {
      "value": 100.0
    }
  }
}
```

判定時の補足:

```json
{
  "avg": 100
}
```
