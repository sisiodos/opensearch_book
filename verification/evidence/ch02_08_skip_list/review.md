# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch02_08_skip_list: PASS

第2章 2.3.4 — skip_list mapping and range

### PUT /lbv-7e280f3b-skip

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
        "type": "long",
        "index": false,
        "skip_list": true
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
  "index": "lbv-7e280f3b-skip"
}
```

### PUT /lbv-7e280f3b-skip/_doc/a?refresh=true

リクエスト:

```json
{
  "v": 8
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-skip",
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

### POST /lbv-7e280f3b-skip/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "range": {
      "v": {
        "gte": 5
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
    "max_score": 1.0,
    "hits": [
      {
        "_index": "lbv-7e280f3b-skip",
        "_id": "a",
        "_score": 1.0,
        "_source": {
          "v": 8
        }
      }
    ]
  }
}
```

### GET /lbv-7e280f3b-skip/_mapping

応答: HTTP 200

```json
{
  "lbv-7e280f3b-skip": {
    "mappings": {
      "properties": {
        "v": {
          "type": "long",
          "index": false,
          "skip_list": true
        }
      }
    }
  }
}
```

判定時の補足:

```json
{
  "lbv-7e280f3b-skip": {
    "mappings": {
      "properties": {
        "v": {
          "type": "long",
          "index": false,
          "skip_list": true
        }
      }
    }
  }
}
```
