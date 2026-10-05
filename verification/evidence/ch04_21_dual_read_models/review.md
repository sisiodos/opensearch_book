# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch04_21_dual_read_models: PASS

第4章 4.3 — product and SKU indexes from same source

### PUT /lbv-7e280f3b-productmodel

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "product": {
        "type": "keyword"
      },
      "skus": {
        "type": "nested",
        "properties": {
          "sku": {
            "type": "keyword"
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
  "index": "lbv-7e280f3b-productmodel"
}
```

### PUT /lbv-7e280f3b-skumodel

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "product": {
        "type": "keyword"
      },
      "sku": {
        "type": "keyword"
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
  "index": "lbv-7e280f3b-skumodel"
}
```

### PUT /lbv-7e280f3b-productmodel/_doc/p1?refresh=true

リクエスト:

```json
{
  "product": "p1",
  "skus": [
    {
      "sku": "s1"
    },
    {
      "sku": "s2"
    }
  ]
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-productmodel",
  "_id": "p1",
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

### PUT /lbv-7e280f3b-skumodel/_doc/s1?refresh=true

リクエスト:

```json
{
  "product": "p1",
  "sku": "s1"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-skumodel",
  "_id": "s1",
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

### PUT /lbv-7e280f3b-skumodel/_doc/s2?refresh=true

リクエスト:

```json
{
  "product": "p1",
  "sku": "s2"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-skumodel",
  "_id": "s2",
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

### POST /lbv-7e280f3b-productmodel/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "match_all": {}
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
        "_index": "lbv-7e280f3b-productmodel",
        "_id": "p1",
        "_score": 1.0,
        "_source": {
          "product": "p1",
          "skus": [
            {
              "sku": "s1"
            },
            {
              "sku": "s2"
            }
          ]
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-skumodel/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "match_all": {}
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
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "lbv-7e280f3b-skumodel",
        "_id": "s1",
        "_score": 1.0,
        "_source": {
          "product": "p1",
          "sku": "s1"
        }
      },
      {
        "_index": "lbv-7e280f3b-skumodel",
        "_id": "s2",
        "_score": 1.0,
        "_source": {
          "product": "p1",
          "sku": "s2"
        }
      }
    ]
  }
}
```

判定時の補足:

```json
{
  "products": 1,
  "skus": 2
}
```
