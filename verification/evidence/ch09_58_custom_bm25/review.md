# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch09_58_custom_bm25: PASS

第9章 9.3.4 — custom BM25 k1/b settings change score

### PUT /lbv-7e280f3b-bma

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0,
    "similarity": {
      "book": {
        "type": "BM25",
        "k1": 1.2,
        "b": 0.75
      }
    }
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "whitespace",
        "similarity": "book"
      },
      "body": {
        "type": "text",
        "analyzer": "whitespace",
        "similarity": "book"
      },
      "popularity": {
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
  "index": "lbv-7e280f3b-bma"
}
```

### PUT /lbv-7e280f3b-bma/_doc/a?refresh=true

リクエスト:

```json
{
  "title": "lucene lucene",
  "body": "lucene lucene",
  "popularity": 4
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-bma",
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

### PUT /lbv-7e280f3b-bma/_doc/b?refresh=true

リクエスト:

```json
{
  "title": "lucene extra extra extra",
  "body": "lucene extra extra extra",
  "popularity": 4
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-bma",
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

### PUT /lbv-7e280f3b-bma/_doc/c?refresh=true

リクエスト:

```json
{
  "title": "other",
  "body": "other",
  "popularity": 4
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-bma",
  "_id": "c",
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

### PUT /lbv-7e280f3b-bmb

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0,
    "similarity": {
      "book": {
        "type": "BM25",
        "k1": 2,
        "b": 0
      }
    }
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "whitespace",
        "similarity": "book"
      },
      "body": {
        "type": "text",
        "analyzer": "whitespace",
        "similarity": "book"
      },
      "popularity": {
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
  "index": "lbv-7e280f3b-bmb"
}
```

### PUT /lbv-7e280f3b-bmb/_doc/a?refresh=true

リクエスト:

```json
{
  "title": "lucene lucene",
  "body": "lucene lucene",
  "popularity": 4
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-bmb",
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

### PUT /lbv-7e280f3b-bmb/_doc/b?refresh=true

リクエスト:

```json
{
  "title": "lucene extra extra extra",
  "body": "lucene extra extra extra",
  "popularity": 4
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-bmb",
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

### PUT /lbv-7e280f3b-bmb/_doc/c?refresh=true

リクエスト:

```json
{
  "title": "other",
  "body": "other",
  "popularity": 4
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-bmb",
  "_id": "c",
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

### POST /lbv-7e280f3b-bma/_search

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
    "max_score": 0.30604887,
    "hits": [
      {
        "_index": "lbv-7e280f3b-bma",
        "_id": "a",
        "_score": 0.30604887,
        "_source": {
          "title": "lucene lucene",
          "body": "lucene lucene",
          "popularity": 4
        }
      },
      {
        "_index": "lbv-7e280f3b-bma",
        "_id": "b",
        "_score": 0.1653279,
        "_source": {
          "title": "lucene extra extra extra",
          "body": "lucene extra extra extra",
          "popularity": 4
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-bmb/_search

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
    "max_score": 0.23500182,
    "hits": [
      {
        "_index": "lbv-7e280f3b-bmb",
        "_id": "a",
        "_score": 0.23500182,
        "_source": {
          "title": "lucene lucene",
          "body": "lucene lucene",
          "popularity": 4
        }
      },
      {
        "_index": "lbv-7e280f3b-bmb",
        "_id": "b",
        "_score": 0.15666789,
        "_source": {
          "title": "lucene extra extra extra",
          "body": "lucene extra extra extra",
          "popularity": 4
        }
      }
    ]
  }
}
```

判定時の補足:

```json
{
  "default": 0.30604887,
  "custom": 0.23500182
}
```
