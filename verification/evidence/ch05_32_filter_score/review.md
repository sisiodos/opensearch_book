# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch05_32_filter_score: PASS

第5章 5.10 — filter does not add score

### PUT /lbv-7e280f3b-filter

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text"
      },
      "available": {
        "type": "boolean"
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
  "index": "lbv-7e280f3b-filter"
}
```

### PUT /lbv-7e280f3b-filter/_doc/a?refresh=true

リクエスト:

```json
{
  "title": "lucene",
  "available": true
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-filter",
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

### PUT /lbv-7e280f3b-filter/_doc/b?refresh=true

リクエスト:

```json
{
  "title": "lucene",
  "available": false
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-filter",
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

### POST /lbv-7e280f3b-filter/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "match": {
      "title": "lucene"
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
    "max_score": 0.082873434,
    "hits": [
      {
        "_index": "lbv-7e280f3b-filter",
        "_id": "a",
        "_score": 0.082873434,
        "_source": {
          "title": "lucene",
          "available": true
        }
      },
      {
        "_index": "lbv-7e280f3b-filter",
        "_id": "b",
        "_score": 0.082873434,
        "_source": {
          "title": "lucene",
          "available": false
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-filter/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "bool": {
      "must": {
        "match": {
          "title": "lucene"
        }
      },
      "filter": {
        "term": {
          "available": true
        }
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
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.082873434,
    "hits": [
      {
        "_index": "lbv-7e280f3b-filter",
        "_id": "a",
        "_score": 0.082873434,
        "_source": {
          "title": "lucene",
          "available": true
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
