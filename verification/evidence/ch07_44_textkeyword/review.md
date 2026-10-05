# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch07_44_textkeyword: PASS

第7章 7.1.3 — text with keyword analyzer remains text without aggregation

### PUT /lbv-7e280f3b-textkeyword

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "v": {
        "type": "text",
        "analyzer": "keyword"
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
  "index": "lbv-7e280f3b-textkeyword"
}
```

### PUT /lbv-7e280f3b-textkeyword/_doc/a?refresh=true

リクエスト:

```json
{
  "v": "OpenSearch Lucene"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-textkeyword",
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

### POST /lbv-7e280f3b-textkeyword/_analyze

リクエスト:

```json
{
  "field": "v",
  "text": "OpenSearch Lucene"
}
```

応答: HTTP 200

```json
{
  "tokens": [
    {
      "token": "OpenSearch Lucene",
      "start_offset": 0,
      "end_offset": 17,
      "type": "word",
      "position": 0
    }
  ]
}
```

### POST /lbv-7e280f3b-textkeyword/_search

リクエスト:

```json
{
  "aggs": {
    "a": {
      "terms": {
        "field": "v"
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
        "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [v] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
      }
    ],
    "type": "search_phase_execution_exception",
    "reason": "all shards failed",
    "phase": "query",
    "grouped": true,
    "failed_shards": [
      {
        "shard": 0,
        "index": "lbv-7e280f3b-textkeyword",
        "node": "p_F7jBWOQHKoSIT3TrF0ig",
        "reason": {
          "type": "illegal_argument_exception",
          "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [v] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
        }
      }
    ],
    "caused_by": {
      "type": "illegal_argument_exception",
      "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [v] in order to load field data by uninverting the inverted index. Note that this can use significant memory.",
      "caused_by": {
        "type": "illegal_argument_exception",
        "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [v] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
      }
    }
  },
  "status": 400
}
```

判定時の補足:

```json
{
  "root_cause": [
    {
      "type": "illegal_argument_exception",
      "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [v] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
    }
  ],
  "type": "search_phase_execution_exception",
  "reason": "all shards failed",
  "phase": "query",
  "grouped": true,
  "failed_shards": [
    {
      "shard": 0,
      "index": "lbv-7e280f3b-textkeyword",
      "node": "p_F7jBWOQHKoSIT3TrF0ig",
      "reason": {
        "type": "illegal_argument_exception",
        "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [v] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
      }
    }
  ],
  "caused_by": {
    "type": "illegal_argument_exception",
    "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [v] in order to load field data by uninverting the inverted index. Note that this can use significant memory.",
    "caused_by": {
      "type": "illegal_argument_exception",
      "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [v] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
    }
  }
}
```
