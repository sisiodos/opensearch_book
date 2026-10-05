# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch05_29_function_scores: PASS

第5章 5.9 — log1p multiply yields zero for zero/missing count

### PUT /lbv-7e280f3b-scores

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "product_name": {
        "type": "text"
      },
      "review_count": {
        "type": "integer"
      },
      "rating": {
        "type": "float"
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
  "index": "lbv-7e280f3b-scores"
}
```

### PUT /lbv-7e280f3b-scores/_doc/zero?refresh=true

リクエスト:

```json
{
  "product_name": "ワイヤレスイヤホン",
  "rating": 4,
  "review_count": 0
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-scores",
  "_id": "zero",
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

### PUT /lbv-7e280f3b-scores/_doc/nine?refresh=true

リクエスト:

```json
{
  "product_name": "ワイヤレスイヤホン",
  "rating": 4,
  "review_count": 9
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-scores",
  "_id": "nine",
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

### PUT /lbv-7e280f3b-scores/_doc/missing?refresh=true

リクエスト:

```json
{
  "product_name": "ワイヤレスイヤホン",
  "rating": 4
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-scores",
  "_id": "missing",
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

### POST /lbv-7e280f3b-scores/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "function_score": {
      "query": {
        "match": {
          "product_name": "ワイヤレスイヤホン"
        }
      },
      "field_value_factor": {
        "field": "review_count",
        "factor": 1.0,
        "modifier": "log1p",
        "missing": 0
      },
      "boost_mode": "multiply"
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
      "value": 3,
      "relation": "eq"
    },
    "max_score": 0.06069608,
    "hits": [
      {
        "_index": "lbv-7e280f3b-scores",
        "_id": "nine",
        "_score": 0.06069608,
        "_source": {
          "product_name": "ワイヤレスイヤホン",
          "rating": 4,
          "review_count": 9
        }
      },
      {
        "_index": "lbv-7e280f3b-scores",
        "_id": "zero",
        "_score": 0.0,
        "_source": {
          "product_name": "ワイヤレスイヤホン",
          "rating": 4,
          "review_count": 0
        }
      },
      {
        "_index": "lbv-7e280f3b-scores",
        "_id": "missing",
        "_score": 0.0,
        "_source": {
          "product_name": "ワイヤレスイヤホン",
          "rating": 4
        }
      }
    ]
  }
}
```

判定時の補足:

```json
{
  "nine": 0.06069608,
  "zero": 0.0,
  "missing": 0.0
}
```
