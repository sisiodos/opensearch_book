# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch06_38_scalar_pairs: PASS

第6章 6.2.3 — application scalar pair key exact match

### PUT /lbv-7e280f3b-pairs

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "segment_keys": {
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
  "index": "lbv-7e280f3b-pairs"
}
```

### PUT /lbv-7e280f3b-pairs/_doc/a?refresh=true

リクエスト:

```json
{
  "segment_keys": [
    "東京-京都",
    "京都-大阪"
  ]
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-pairs",
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

### POST /lbv-7e280f3b-pairs/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "term": {
      "segment_keys": "東京-京都"
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
        "_index": "lbv-7e280f3b-pairs",
        "_id": "a",
        "_score": 1.0,
        "_source": {
          "segment_keys": [
            "東京-京都",
            "京都-大阪"
          ]
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-pairs/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "term": {
      "segment_keys": "東京-大阪"
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
      "value": 0,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  }
}
```

判定時の補足:

```json
null
```
