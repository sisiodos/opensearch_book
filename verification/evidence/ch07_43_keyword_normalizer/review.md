# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch07_43_keyword_normalizer: PASS

第7章 7.1.3 — keyword rejects analyzer; normalizer retains one term

### PUT /lbv-7e280f3b-badkw

リクエスト:

```json
{
  "mappings": {
    "properties": {
      "k": {
        "type": "keyword",
        "analyzer": "standard"
      }
    }
  }
}
```

応答: HTTP 400

```json
{
  "error": {
    "root_cause": [
      {
        "type": "mapper_parsing_exception",
        "reason": "unknown parameter [analyzer] on mapper [k] of type [keyword]"
      }
    ],
    "type": "mapper_parsing_exception",
    "reason": "Failed to parse mapping [_doc]: unknown parameter [analyzer] on mapper [k] of type [keyword]",
    "caused_by": {
      "type": "mapper_parsing_exception",
      "reason": "unknown parameter [analyzer] on mapper [k] of type [keyword]"
    }
  },
  "status": 400
}
```

### PUT /lbv-7e280f3b-norm

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0,
    "analysis": {
      "normalizer": {
        "lower": {
          "type": "custom",
          "filter": [
            "lowercase"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "k": {
        "type": "keyword",
        "normalizer": "lower"
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
  "index": "lbv-7e280f3b-norm"
}
```

### PUT /lbv-7e280f3b-norm/_doc/a?refresh=true

リクエスト:

```json
{
  "k": "OpenSearch Lucene"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-norm",
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

### POST /lbv-7e280f3b-norm/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "term": {
      "k": "OPENSEARCH LUCENE"
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
        "_index": "lbv-7e280f3b-norm",
        "_id": "a",
        "_score": 1.0,
        "_source": {
          "k": "OpenSearch Lucene"
        }
      }
    ]
  }
}
```

判定時の補足:

```json
{
  "root_cause": [
    {
      "type": "mapper_parsing_exception",
      "reason": "unknown parameter [analyzer] on mapper [k] of type [keyword]"
    }
  ],
  "type": "mapper_parsing_exception",
  "reason": "Failed to parse mapping [_doc]: unknown parameter [analyzer] on mapper [k] of type [keyword]",
  "caused_by": {
    "type": "mapper_parsing_exception",
    "reason": "unknown parameter [analyzer] on mapper [k] of type [keyword]"
  }
}
```
