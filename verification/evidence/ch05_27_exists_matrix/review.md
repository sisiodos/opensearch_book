# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch05_27_exists_matrix: PASS

第5章 5.8 — exists/null/empty/ignore_above behavior

### PUT /lbv-7e280f3b-exists

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "v": {
        "type": "keyword",
        "ignore_above": 5
      },
      "dv": {
        "type": "keyword",
        "index": false
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
  "index": "lbv-7e280f3b-exists"
}
```

### PUT /lbv-7e280f3b-exists/_doc/null?refresh=true

リクエスト:

```json
{
  "v": null
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-exists",
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

### PUT /lbv-7e280f3b-exists/_doc/missing?refresh=true

リクエスト:

```json
{}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-exists",
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

### PUT /lbv-7e280f3b-exists/_doc/emptyarray?refresh=true

リクエスト:

```json
{
  "v": []
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-exists",
  "_id": "emptyarray",
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

### PUT /lbv-7e280f3b-exists/_doc/emptystr?refresh=true

リクエスト:

```json
{
  "v": ""
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-exists",
  "_id": "emptystr",
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

### PUT /lbv-7e280f3b-exists/_doc/array?refresh=true

リクエスト:

```json
{
  "v": [
    null,
    "one"
  ]
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-exists",
  "_id": "array",
  "_version": 1,
  "result": "created",
  "forced_refresh": true,
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 4,
  "_primary_term": 1
}
```

### PUT /lbv-7e280f3b-exists/_doc/long?refresh=true

リクエスト:

```json
{
  "v": "too-long"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-exists",
  "_id": "long",
  "_version": 1,
  "result": "created",
  "forced_refresh": true,
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 5,
  "_primary_term": 1
}
```

### PUT /lbv-7e280f3b-exists/_doc/dv?refresh=true

リクエスト:

```json
{
  "dv": "exists"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-exists",
  "_id": "dv",
  "_version": 1,
  "result": "created",
  "forced_refresh": true,
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 6,
  "_primary_term": 1
}
```

### POST /lbv-7e280f3b-exists/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "exists": {
      "field": "v"
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
        "_index": "lbv-7e280f3b-exists",
        "_id": "emptystr",
        "_score": 1.0,
        "_source": {
          "v": ""
        }
      },
      {
        "_index": "lbv-7e280f3b-exists",
        "_id": "array",
        "_score": 1.0,
        "_source": {
          "v": [
            null,
            "one"
          ]
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-exists/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "exists": {
      "field": "dv"
    }
  }
}
```

応答: HTTP 200

```json
{
  "took": 0,
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
        "_index": "lbv-7e280f3b-exists",
        "_id": "dv",
        "_score": 1.0,
        "_source": {
          "dv": "exists"
        }
      }
    ]
  }
}
```

判定時の補足:

```json
{
  "source_null_not_same_as_not_exists": true
}
```
