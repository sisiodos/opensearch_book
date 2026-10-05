# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch07_49_query_types: PASS

第7章 7.4.1 — term/match/phrase/prefix/wildcard/regexp differences

### PUT /lbv-7e280f3b-types

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "t": {
        "type": "text"
      },
      "k": {
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
  "index": "lbv-7e280f3b-types"
}
```

### PUT /lbv-7e280f3b-types/_doc/a?refresh=true

リクエスト:

```json
{
  "t": "OpenSearch Lucene",
  "k": "OpenSearch Lucene"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-types",
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

### PUT /lbv-7e280f3b-types/_doc/b?refresh=true

リクエスト:

```json
{
  "t": "Lucene OpenSearch",
  "k": "Lucene OpenSearch"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-types",
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

### POST /lbv-7e280f3b-types/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "term": {
      "t": "Lucene"
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

### POST /lbv-7e280f3b-types/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "match": {
      "t": "Lucene"
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
        "_index": "lbv-7e280f3b-types",
        "_id": "a",
        "_score": 0.082873434,
        "_source": {
          "t": "OpenSearch Lucene",
          "k": "OpenSearch Lucene"
        }
      },
      {
        "_index": "lbv-7e280f3b-types",
        "_id": "b",
        "_score": 0.082873434,
        "_source": {
          "t": "Lucene OpenSearch",
          "k": "Lucene OpenSearch"
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-types/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "match_phrase": {
      "t": "OpenSearch Lucene"
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
    "max_score": 0.16574687,
    "hits": [
      {
        "_index": "lbv-7e280f3b-types",
        "_id": "a",
        "_score": 0.16574687,
        "_source": {
          "t": "OpenSearch Lucene",
          "k": "OpenSearch Lucene"
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-types/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "prefix": {
      "k": "Open"
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
        "_index": "lbv-7e280f3b-types",
        "_id": "a",
        "_score": 1.0,
        "_source": {
          "t": "OpenSearch Lucene",
          "k": "OpenSearch Lucene"
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-types/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "wildcard": {
      "k": "*Lucene"
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
        "_index": "lbv-7e280f3b-types",
        "_id": "a",
        "_score": 1.0,
        "_source": {
          "t": "OpenSearch Lucene",
          "k": "OpenSearch Lucene"
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-types/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "regexp": {
      "k": "Open.*"
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
        "_index": "lbv-7e280f3b-types",
        "_id": "a",
        "_score": 1.0,
        "_source": {
          "t": "OpenSearch Lucene",
          "k": "OpenSearch Lucene"
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
