# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch03_16_four_combinations: PASS

第3章 3.4–3.5 — index/doc_values four combinations

### PUT /lbv-7e280f3b-combos

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "v00": {
        "type": "integer",
        "index": false,
        "doc_values": false
      },
      "v01": {
        "type": "integer",
        "index": false,
        "doc_values": true
      },
      "v10": {
        "type": "integer",
        "index": true,
        "doc_values": false
      },
      "v11": {
        "type": "integer",
        "index": true,
        "doc_values": true
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
  "index": "lbv-7e280f3b-combos"
}
```

### PUT /lbv-7e280f3b-combos/_doc/a?refresh=true

リクエスト:

```json
{
  "v00": 5,
  "v01": 5,
  "v10": 5,
  "v11": 5
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-combos",
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

### POST /lbv-7e280f3b-combos/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "term": {
      "v01": 5
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
        "_index": "lbv-7e280f3b-combos",
        "_id": "a",
        "_score": 1.0,
        "_source": {
          "v00": 5,
          "v01": 5,
          "v10": 5,
          "v11": 5
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-combos/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "term": {
      "v10": 5
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
        "_index": "lbv-7e280f3b-combos",
        "_id": "a",
        "_score": 1.0,
        "_source": {
          "v00": 5,
          "v01": 5,
          "v10": 5,
          "v11": 5
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-combos/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "term": {
      "v11": 5
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
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "lbv-7e280f3b-combos",
        "_id": "a",
        "_score": 1.0,
        "_source": {
          "v00": 5,
          "v01": 5,
          "v10": 5,
          "v11": 5
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-combos/_search

リクエスト:

```json
{
  "query": {
    "term": {
      "v00": 5
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
        "type": "query_shard_exception",
        "reason": "failed to create query: Cannot search on field [v00] since it is both not indexed, and does not have doc_values enabled.",
        "index": "lbv-7e280f3b-combos",
        "index_uuid": "orO-rMFyR_KuLtR4_rJuTw"
      }
    ],
    "type": "search_phase_execution_exception",
    "reason": "all shards failed",
    "phase": "query",
    "grouped": true,
    "failed_shards": [
      {
        "shard": 0,
        "index": "lbv-7e280f3b-combos",
        "node": "p_F7jBWOQHKoSIT3TrF0ig",
        "reason": {
          "type": "query_shard_exception",
          "reason": "failed to create query: Cannot search on field [v00] since it is both not indexed, and does not have doc_values enabled.",
          "index": "lbv-7e280f3b-combos",
          "index_uuid": "orO-rMFyR_KuLtR4_rJuTw",
          "caused_by": {
            "type": "illegal_argument_exception",
            "reason": "Cannot search on field [v00] since it is both not indexed, and does not have doc_values enabled."
          }
        }
      }
    ],
    "caused_by": {
      "type": "query_shard_exception",
      "reason": "failed to create query: Cannot search on field [v00] since it is both not indexed, and does not have doc_values enabled.",
      "index": "lbv-7e280f3b-combos",
      "index_uuid": "orO-rMFyR_KuLtR4_rJuTw",
      "caused_by": {
        "type": "illegal_argument_exception",
        "reason": "Cannot search on field [v00] since it is both not indexed, and does not have doc_values enabled."
      }
    }
  },
  "status": 400
}
```

### POST /lbv-7e280f3b-combos/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "match_all": {}
  },
  "aggs": {
    "a": {
      "avg": {
        "field": "v01"
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
        "_index": "lbv-7e280f3b-combos",
        "_id": "a",
        "_score": 1.0,
        "_source": {
          "v00": 5,
          "v01": 5,
          "v10": 5,
          "v11": 5
        }
      }
    ]
  },
  "aggregations": {
    "a": {
      "value": 5.0
    }
  }
}
```

### POST /lbv-7e280f3b-combos/_search

リクエスト:

```json
{
  "aggs": {
    "a": {
      "avg": {
        "field": "v10"
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
        "type": "illegal_argument_exception",
        "reason": "Can't load fielddata on [v10] because fielddata is unsupported on fields of type [integer]. Use doc values instead."
      }
    ],
    "type": "search_phase_execution_exception",
    "reason": "all shards failed",
    "phase": "query",
    "grouped": true,
    "failed_shards": [
      {
        "shard": 0,
        "index": "lbv-7e280f3b-combos",
        "node": "p_F7jBWOQHKoSIT3TrF0ig",
        "reason": {
          "type": "illegal_argument_exception",
          "reason": "Can't load fielddata on [v10] because fielddata is unsupported on fields of type [integer]. Use doc values instead."
        }
      }
    ],
    "caused_by": {
      "type": "illegal_argument_exception",
      "reason": "Can't load fielddata on [v10] because fielddata is unsupported on fields of type [integer]. Use doc values instead.",
      "caused_by": {
        "type": "illegal_argument_exception",
        "reason": "Can't load fielddata on [v10] because fielddata is unsupported on fields of type [integer]. Use doc values instead."
      }
    }
  },
  "status": 400
}
```

判定時の補足:

```json
null
```
