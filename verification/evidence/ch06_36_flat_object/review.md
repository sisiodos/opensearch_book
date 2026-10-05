# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch06_36_flat_object: PASS

第6章 6.1.3 — flat_object keeps keys out of mapping and exact lookup

### PUT /lbv-7e280f3b-flat

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "price": {
        "type": "integer"
      },
      "attributes": {
        "type": "flat_object"
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
  "index": "lbv-7e280f3b-flat"
}
```

### PUT /lbv-7e280f3b-flat/_doc/a?refresh=true

リクエスト:

```json
{
  "price": 100,
  "attributes": {
    "custom_001": "red",
    "n": "100"
  }
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-flat",
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

### PUT /lbv-7e280f3b-flat/_doc/b?refresh=true

リクエスト:

```json
{
  "price": 20,
  "attributes": {
    "custom_002": "blue",
    "n": "20"
  }
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-flat",
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

### GET /lbv-7e280f3b-flat/_mapping

応答: HTTP 200

```json
{
  "lbv-7e280f3b-flat": {
    "mappings": {
      "properties": {
        "attributes": {
          "type": "flat_object"
        },
        "price": {
          "type": "integer"
        }
      }
    }
  }
}
```

### POST /lbv-7e280f3b-flat/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "term": {
      "attributes.custom_001": "red"
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
        "_index": "lbv-7e280f3b-flat",
        "_id": "a",
        "_score": 1.0,
        "_source": {
          "price": 100,
          "attributes": {
            "custom_001": "red",
            "n": "100"
          }
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-flat/_search

リクエスト:

```json
{
  "aggs": {
    "a": {
      "terms": {
        "field": "attributes.custom_001"
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
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "lbv-7e280f3b-flat",
        "_id": "a",
        "_score": 1.0,
        "_source": {
          "price": 100,
          "attributes": {
            "custom_001": "red",
            "n": "100"
          }
        }
      },
      {
        "_index": "lbv-7e280f3b-flat",
        "_id": "b",
        "_score": 1.0,
        "_source": {
          "price": 20,
          "attributes": {
            "custom_002": "blue",
            "n": "20"
          }
        }
      }
    ]
  },
  "aggregations": {
    "a": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "red",
          "doc_count": 1
        },
        {
          "key": "java.lang.Object@6cce0b1f",
          "doc_count": 1
        },
        {
          "key": "java.lang.Object@6cce0b1f",
          "doc_count": 1
        },
        {
          "key": "java.lang.Object@6cce0b1f",
          "doc_count": 1
        }
      ]
    }
  }
}
```

判定時の補足:

```json
{
  "mapping": {
    "type": "flat_object"
  },
  "internal_aggregation_response": {
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
        "value": 2,
        "relation": "eq"
      },
      "max_score": 1.0,
      "hits": [
        {
          "_index": "lbv-7e280f3b-flat",
          "_id": "a",
          "_score": 1.0,
          "_source": {
            "price": 100,
            "attributes": {
              "custom_001": "red",
              "n": "100"
            }
          }
        },
        {
          "_index": "lbv-7e280f3b-flat",
          "_id": "b",
          "_score": 1.0,
          "_source": {
            "price": 20,
            "attributes": {
              "custom_002": "blue",
              "n": "20"
            }
          }
        }
      ]
    },
    "aggregations": {
      "a": {
        "doc_count_error_upper_bound": 0,
        "sum_other_doc_count": 0,
        "buckets": [
          {
            "key": "red",
            "doc_count": 1
          },
          {
            "key": "java.lang.Object@6cce0b1f",
            "doc_count": 1
          },
          {
            "key": "java.lang.Object@6cce0b1f",
            "doc_count": 1
          },
          {
            "key": "java.lang.Object@6cce0b1f",
            "doc_count": 1
          }
        ]
      }
    }
  }
}
```
