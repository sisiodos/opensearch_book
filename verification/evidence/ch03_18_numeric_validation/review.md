# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch03_18_numeric_validation: PASS

第3章 3.5 — index false still validates numeric input

### PUT /lbv-7e280f3b-validate

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
        "type": "integer",
        "index": false,
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
  "index": "lbv-7e280f3b-validate"
}
```

### PUT /lbv-7e280f3b-validate/_doc/a

リクエスト:

```json
{
  "v": "not-a-number"
}
```

応答: HTTP 400

```json
{
  "error": {
    "root_cause": [
      {
        "type": "mapper_parsing_exception",
        "reason": "failed to parse field [v] of type [integer] in document with id 'a'. Preview of field's value: 'not-a-number'"
      }
    ],
    "type": "mapper_parsing_exception",
    "reason": "failed to parse field [v] of type [integer] in document with id 'a'. Preview of field's value: 'not-a-number'",
    "caused_by": {
      "type": "number_format_exception",
      "reason": "For input string: \"not-a-number\""
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
      "type": "mapper_parsing_exception",
      "reason": "failed to parse field [v] of type [integer] in document with id 'a'. Preview of field's value: 'not-a-number'"
    }
  ],
  "type": "mapper_parsing_exception",
  "reason": "failed to parse field [v] of type [integer] in document with id 'a'. Preview of field's value: 'not-a-number'",
  "caused_by": {
    "type": "number_format_exception",
    "reason": "For input string: \"not-a-number\""
  }
}
```
