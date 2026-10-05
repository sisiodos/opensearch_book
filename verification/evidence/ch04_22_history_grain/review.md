# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch04_22_history_grain: PASS

第4章 4.5 — history document count differs from people count

### PUT /lbv-7e280f3b-history

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "user": {
        "type": "keyword"
      },
      "score": {
        "type": "integer"
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
  "index": "lbv-7e280f3b-history"
}
```

### PUT /lbv-7e280f3b-history/_doc/h1?refresh=true

リクエスト:

```json
{
  "user": "u1",
  "score": 86
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-history",
  "_id": "h1",
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

### PUT /lbv-7e280f3b-history/_doc/h2?refresh=true

リクエスト:

```json
{
  "user": "u1",
  "score": 86
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-history",
  "_id": "h2",
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

### PUT /lbv-7e280f3b-history/_doc/h3?refresh=true

リクエスト:

```json
{
  "user": "u2",
  "score": 86
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-history",
  "_id": "h3",
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

### POST /lbv-7e280f3b-history/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "match_all": {}
  },
  "aggs": {
    "people": {
      "cardinality": {
        "field": "user"
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
      "value": 3,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "lbv-7e280f3b-history",
        "_id": "h1",
        "_score": 1.0,
        "_source": {
          "user": "u1",
          "score": 86
        }
      },
      {
        "_index": "lbv-7e280f3b-history",
        "_id": "h2",
        "_score": 1.0,
        "_source": {
          "user": "u1",
          "score": 86
        }
      },
      {
        "_index": "lbv-7e280f3b-history",
        "_id": "h3",
        "_score": 1.0,
        "_source": {
          "user": "u2",
          "score": 86
        }
      }
    ]
  },
  "aggregations": {
    "people": {
      "value": 2
    }
  }
}
```

判定時の補足:

```json
{
  "histories": 3,
  "people": 2
}
```
