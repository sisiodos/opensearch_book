# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch05_31_stock: PASS

第5章 5.10 — exists inventory vs quantity > 0

### PUT /lbv-7e280f3b-stock

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "stock": {
        "properties": {
          "quantity": {
            "type": "integer"
          }
        }
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
  "index": "lbv-7e280f3b-stock"
}
```

### PUT /lbv-7e280f3b-stock/_doc/zero?refresh=true

リクエスト:

```json
{
  "stock": {
    "quantity": 0
  }
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-stock",
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

### PUT /lbv-7e280f3b-stock/_doc/negative?refresh=true

リクエスト:

```json
{
  "stock": {
    "quantity": -1
  }
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-stock",
  "_id": "negative",
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

### PUT /lbv-7e280f3b-stock/_doc/positive?refresh=true

リクエスト:

```json
{
  "stock": {
    "quantity": 2
  }
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-stock",
  "_id": "positive",
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

### PUT /lbv-7e280f3b-stock/_doc/missing?refresh=true

リクエスト:

```json
{}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-stock",
  "_id": "missing",
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

### POST /lbv-7e280f3b-stock/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "exists": {
      "field": "stock.quantity"
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
      "value": 3,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "lbv-7e280f3b-stock",
        "_id": "zero",
        "_score": 1.0,
        "_source": {
          "stock": {
            "quantity": 0
          }
        }
      },
      {
        "_index": "lbv-7e280f3b-stock",
        "_id": "negative",
        "_score": 1.0,
        "_source": {
          "stock": {
            "quantity": -1
          }
        }
      },
      {
        "_index": "lbv-7e280f3b-stock",
        "_id": "positive",
        "_score": 1.0,
        "_source": {
          "stock": {
            "quantity": 2
          }
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-stock/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "range": {
      "stock.quantity": {
        "gt": 0
      }
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
        "_index": "lbv-7e280f3b-stock",
        "_id": "positive",
        "_score": 1.0,
        "_source": {
          "stock": {
            "quantity": 2
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
