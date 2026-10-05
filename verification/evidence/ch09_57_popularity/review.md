# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch09_57_popularity: PASS

第9章 9.3.3 — sqrt(factor * popularity) multiply formula

### PUT /lbv-7e280f3b-popularity

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
  "index": "lbv-7e280f3b-popularity"
}
```

### PUT /lbv-7e280f3b-popularity/_doc/a?refresh=true

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
  "_index": "lbv-7e280f3b-popularity",
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

### PUT /lbv-7e280f3b-popularity/_doc/b?refresh=true

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
  "_index": "lbv-7e280f3b-popularity",
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

### PUT /lbv-7e280f3b-popularity/_doc/c?refresh=true

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
  "_index": "lbv-7e280f3b-popularity",
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

### PUT /lbv-7e280f3b-popularity/_doc/a?refresh=true

リクエスト:

```json
{
  "title": "OpenSearch",
  "body": "other",
  "popularity": 4
}
```

応答: HTTP 200

```json
{
  "_index": "lbv-7e280f3b-popularity",
  "_id": "a",
  "_version": 2,
  "result": "updated",
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

### POST /lbv-7e280f3b-popularity/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "match": {
      "title": "OpenSearch"
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
    "max_score": 0.6879845,
    "hits": [
      {
        "_index": "lbv-7e280f3b-popularity",
        "_id": "a",
        "_score": 0.6879845,
        "_source": {
          "title": "OpenSearch",
          "body": "other",
          "popularity": 4
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-popularity/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "function_score": {
      "query": {
        "match": {
          "title": "OpenSearch"
        }
      },
      "field_value_factor": {
        "field": "popularity",
        "modifier": "sqrt",
        "factor": 1.5
      },
      "boost_mode": "multiply"
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
    "max_score": 1.6852111,
    "hits": [
      {
        "_index": "lbv-7e280f3b-popularity",
        "_id": "a",
        "_score": 1.6852111,
        "_source": {
          "title": "OpenSearch",
          "body": "other",
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
  "actual": 1.6852111,
  "expected": 1.6852109759438132
}
```
