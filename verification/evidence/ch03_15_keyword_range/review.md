# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch03_15_keyword_range: PASS

第3章 3.4 — keyword lexicographic range differs from numeric

### PUT /lbv-7e280f3b-lex

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "s": {
        "type": "keyword"
      },
      "n": {
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
  "index": "lbv-7e280f3b-lex"
}
```

### PUT /lbv-7e280f3b-lex/_doc/20?refresh=true

リクエスト:

```json
{
  "s": "20",
  "n": 20
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-lex",
  "_id": "20",
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

### PUT /lbv-7e280f3b-lex/_doc/100?refresh=true

リクエスト:

```json
{
  "s": "100",
  "n": 100
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-lex",
  "_id": "100",
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

### POST /lbv-7e280f3b-lex/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "range": {
      "s": {
        "lt": "20"
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
        "_index": "lbv-7e280f3b-lex",
        "_id": "100",
        "_score": 1.0,
        "_source": {
          "s": "100",
          "n": 100
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-lex/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "range": {
      "n": {
        "lt": 20
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
