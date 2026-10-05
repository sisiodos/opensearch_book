# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch05_28_null_value: PASS

第5章 5.8 — null_value distinguishes explicit null from missing

### PUT /lbv-7e280f3b-nullvalue

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "price": {
        "type": "float",
        "null_value": -1
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
  "index": "lbv-7e280f3b-nullvalue"
}
```

### PUT /lbv-7e280f3b-nullvalue/_doc/null?refresh=true

リクエスト:

```json
{
  "price": null
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-nullvalue",
  "_id": "null",
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

### PUT /lbv-7e280f3b-nullvalue/_doc/missing?refresh=true

リクエスト:

```json
{}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-nullvalue",
  "_id": "missing",
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

### PUT /lbv-7e280f3b-nullvalue/_doc/empty?refresh=true

リクエスト:

```json
{
  "price": []
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-nullvalue",
  "_id": "empty",
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

### PUT /lbv-7e280f3b-nullvalue/_doc/zero?refresh=true

リクエスト:

```json
{
  "price": 0
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-nullvalue",
  "_id": "zero",
  "_version": 1,
  "result": "created",
  "forced_refresh": true,
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 3,
  "_primary_term": 1
}
```

### POST /lbv-7e280f3b-nullvalue/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "exists": {
      "field": "price"
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
    "max_score": 1.0,
    "hits": [
      {
        "_index": "lbv-7e280f3b-nullvalue",
        "_id": "null",
        "_score": 1.0,
        "_source": {
          "price": null
        }
      },
      {
        "_index": "lbv-7e280f3b-nullvalue",
        "_id": "zero",
        "_score": 1.0,
        "_source": {
          "price": 0
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-nullvalue/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "term": {
      "price": -1
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
    "max_score": 1.0,
    "hits": [
      {
        "_index": "lbv-7e280f3b-nullvalue",
        "_id": "null",
        "_score": 1.0,
        "_source": {
          "price": null
        }
      }
    ]
  }
}
```

### GET /lbv-7e280f3b-nullvalue/_doc/null

応答: HTTP 200

```json
{
  "_index": "lbv-7e280f3b-nullvalue",
  "_id": "null",
  "_version": 1,
  "_seq_no": 0,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "price": null
  }
}
```

判定時の補足:

```json
null
```
