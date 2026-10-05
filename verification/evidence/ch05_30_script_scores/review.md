# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch05_30_script_scores: PASS

第5章 5.9 — script_score replaces lexical score

### PUT /lbv-7e280f3b-script

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
  "index": "lbv-7e280f3b-script"
}
```

### PUT /lbv-7e280f3b-script/_doc/a?refresh=true

リクエスト:

```json
{
  "product_name": "ワイヤレスイヤホン",
  "review_count": 9,
  "rating": 4
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-script",
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

### POST /lbv-7e280f3b-script/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "script_score": {
      "query": {
        "match": {
          "product_name": "ワイヤレスイヤホン"
        }
      },
      "script": {
        "source": "Math.log(2 + doc['review_count'].value) + doc['rating'].value",
        "params": {}
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
    "max_score": 6.3978953,
    "hits": [
      {
        "_index": "lbv-7e280f3b-script",
        "_id": "a",
        "_score": 6.3978953,
        "_source": {
          "product_name": "ワイヤレスイヤホン",
          "review_count": 9,
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
  "actual": 6.3978953,
  "formula": 6.397895272798371
}
```
