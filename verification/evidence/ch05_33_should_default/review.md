# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch05_33_should_default: PASS

第5章 5.10 — should optional only with must/filter by default

### PUT /lbv-7e280f3b-should

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "tag": {
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
  "index": "lbv-7e280f3b-should"
}
```

### PUT /lbv-7e280f3b-should/_doc/a?refresh=true

リクエスト:

```json
{
  "tag": "yes"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-should",
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

### PUT /lbv-7e280f3b-should/_doc/b?refresh=true

リクエスト:

```json
{
  "tag": "no"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-should",
  "_id": "b",
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

### POST /lbv-7e280f3b-should/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "bool": {
      "should": [
        {
          "term": {
            "tag": "yes"
          }
        }
      ]
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
        "_index": "lbv-7e280f3b-should",
        "_id": "a",
        "_score": 1.0,
        "_source": {
          "tag": "yes"
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-should/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "bool": {
      "filter": {
        "match_all": {}
      },
      "should": [
        {
          "term": {
            "tag": "yes"
          }
        }
      ]
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
        "_index": "lbv-7e280f3b-should",
        "_id": "a",
        "_score": 1.0,
        "_source": {
          "tag": "yes"
        }
      },
      {
        "_index": "lbv-7e280f3b-should",
        "_id": "b",
        "_score": 0.0,
        "_source": {
          "tag": "no"
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
