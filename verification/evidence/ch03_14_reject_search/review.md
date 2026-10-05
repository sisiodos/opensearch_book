# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch03_14_reject_search: PASS

第3章 3.4 — text aggregation fails without fielddata

### POST /lbv-7e280f3b-basic/_search

リクエスト:

```json
{
  "aggs": {
    "n": {
      "terms": {
        "field": "name"
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
        "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [name] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
      }
    ],
    "type": "search_phase_execution_exception",
    "reason": "all shards failed",
    "phase": "query",
    "grouped": true,
    "failed_shards": [
      {
        "shard": 0,
        "index": "lbv-7e280f3b-basic",
        "node": "p_F7jBWOQHKoSIT3TrF0ig",
        "reason": {
          "type": "illegal_argument_exception",
          "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [name] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
        }
      }
    ],
    "caused_by": {
      "type": "illegal_argument_exception",
      "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [name] in order to load field data by uninverting the inverted index. Note that this can use significant memory.",
      "caused_by": {
        "type": "illegal_argument_exception",
        "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [name] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
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
      "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [name] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
    }
  ],
  "type": "search_phase_execution_exception",
  "reason": "all shards failed",
  "phase": "query",
  "grouped": true,
  "failed_shards": [
    {
      "shard": 0,
      "index": "lbv-7e280f3b-basic",
      "node": "p_F7jBWOQHKoSIT3TrF0ig",
      "reason": {
        "type": "illegal_argument_exception",
        "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [name] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
      }
    }
  ],
  "caused_by": {
    "type": "illegal_argument_exception",
    "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [name] in order to load field data by uninverting the inverted index. Note that this can use significant memory.",
    "caused_by": {
      "type": "illegal_argument_exception",
      "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [name] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
    }
  }
}
```
