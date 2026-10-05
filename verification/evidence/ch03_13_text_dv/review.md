# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch03_13_text_dv: PASS

第3章 3.2 / 3.4 — text accepts but ignores doc_values true and false

### PUT /lbv-7e280f3b-textdvtrue

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
        "type": "text",
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
  "index": "lbv-7e280f3b-textdvtrue"
}
```

### PUT /lbv-7e280f3b-textdvtrue/_doc/a?refresh=true

リクエスト:

```json
{
  "t": "hello"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-textdvtrue",
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

### GET /lbv-7e280f3b-textdvtrue/_mapping

応答: HTTP 200

```json
{
  "lbv-7e280f3b-textdvtrue": {
    "mappings": {
      "properties": {
        "t": {
          "type": "text"
        }
      }
    }
  }
}
```

### GET /lbv-7e280f3b-textdvtrue/_field_caps?fields=t

応答: HTTP 200

```json
{
  "indices": [
    "lbv-7e280f3b-textdvtrue"
  ],
  "fields": {
    "t": {
      "text": {
        "type": "text",
        "searchable": true,
        "aggregatable": false
      }
    }
  }
}
```

### POST /lbv-7e280f3b-textdvtrue/_search

リクエスト:

```json
{
  "aggs": {
    "t": {
      "terms": {
        "field": "t"
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
        "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [t] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
      }
    ],
    "type": "search_phase_execution_exception",
    "reason": "all shards failed",
    "phase": "query",
    "grouped": true,
    "failed_shards": [
      {
        "shard": 0,
        "index": "lbv-7e280f3b-textdvtrue",
        "node": "p_F7jBWOQHKoSIT3TrF0ig",
        "reason": {
          "type": "illegal_argument_exception",
          "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [t] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
        }
      }
    ],
    "caused_by": {
      "type": "illegal_argument_exception",
      "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [t] in order to load field data by uninverting the inverted index. Note that this can use significant memory.",
      "caused_by": {
        "type": "illegal_argument_exception",
        "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [t] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
      }
    }
  },
  "status": 400
}
```

### PUT /lbv-7e280f3b-textdvfalse

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
        "type": "text",
        "doc_values": false
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
  "index": "lbv-7e280f3b-textdvfalse"
}
```

### PUT /lbv-7e280f3b-textdvfalse/_doc/a?refresh=true

リクエスト:

```json
{
  "t": "hello"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-textdvfalse",
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

### GET /lbv-7e280f3b-textdvfalse/_mapping

応答: HTTP 200

```json
{
  "lbv-7e280f3b-textdvfalse": {
    "mappings": {
      "properties": {
        "t": {
          "type": "text"
        }
      }
    }
  }
}
```

### GET /lbv-7e280f3b-textdvfalse/_field_caps?fields=t

応答: HTTP 200

```json
{
  "indices": [
    "lbv-7e280f3b-textdvfalse"
  ],
  "fields": {
    "t": {
      "text": {
        "type": "text",
        "searchable": true,
        "aggregatable": false
      }
    }
  }
}
```

### POST /lbv-7e280f3b-textdvfalse/_search

リクエスト:

```json
{
  "aggs": {
    "t": {
      "terms": {
        "field": "t"
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
        "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [t] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
      }
    ],
    "type": "search_phase_execution_exception",
    "reason": "all shards failed",
    "phase": "query",
    "grouped": true,
    "failed_shards": [
      {
        "shard": 0,
        "index": "lbv-7e280f3b-textdvfalse",
        "node": "p_F7jBWOQHKoSIT3TrF0ig",
        "reason": {
          "type": "illegal_argument_exception",
          "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [t] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
        }
      }
    ],
    "caused_by": {
      "type": "illegal_argument_exception",
      "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [t] in order to load field data by uninverting the inverted index. Note that this can use significant memory.",
      "caused_by": {
        "type": "illegal_argument_exception",
        "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [t] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
      }
    }
  },
  "status": 400
}
```

判定時の補足:

```json
[
  {
    "input_doc_values": true,
    "mapping": {
      "type": "text"
    },
    "caps": {
      "type": "text",
      "searchable": true,
      "aggregatable": false
    },
    "aggregation_error": {
      "root_cause": [
        {
          "type": "illegal_argument_exception",
          "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [t] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
        }
      ],
      "type": "search_phase_execution_exception",
      "reason": "all shards failed",
      "phase": "query",
      "grouped": true,
      "failed_shards": [
        {
          "shard": 0,
          "index": "lbv-7e280f3b-textdvtrue",
          "node": "p_F7jBWOQHKoSIT3TrF0ig",
          "reason": {
            "type": "illegal_argument_exception",
            "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [t] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
          }
        }
      ],
      "caused_by": {
        "type": "illegal_argument_exception",
        "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [t] in order to load field data by uninverting the inverted index. Note that this can use significant memory.",
        "caused_by": {
          "type": "illegal_argument_exception",
          "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [t] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
        }
      }
    }
  },
  {
    "input_doc_values": false,
    "mapping": {
      "type": "text"
    },
    "caps": {
      "type": "text",
      "searchable": true,
      "aggregatable": false
    },
    "aggregation_error": {
      "root_cause": [
        {
          "type": "illegal_argument_exception",
          "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [t] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
        }
      ],
      "type": "search_phase_execution_exception",
      "reason": "all shards failed",
      "phase": "query",
      "grouped": true,
      "failed_shards": [
        {
          "shard": 0,
          "index": "lbv-7e280f3b-textdvfalse",
          "node": "p_F7jBWOQHKoSIT3TrF0ig",
          "reason": {
            "type": "illegal_argument_exception",
            "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [t] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
          }
        }
      ],
      "caused_by": {
        "type": "illegal_argument_exception",
        "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [t] in order to load field data by uninverting the inverted index. Note that this can use significant memory.",
        "caused_by": {
          "type": "illegal_argument_exception",
          "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [t] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
        }
      }
    }
  }
]
```
