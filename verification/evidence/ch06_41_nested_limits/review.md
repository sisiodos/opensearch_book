# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch06_41_nested_limits: PASS

第6章 6.2.5 — depth/nested_fields/nested_objects limits reject excess

### PUT /lbv-7e280f3b-depth

リクエスト:

```json
{
  "settings": {
    "index.mapping.depth.limit": 1
  },
  "mappings": {
    "properties": {
      "a": {
        "properties": {
          "b": {
            "properties": {
              "c": {
                "type": "keyword"
              }
            }
          }
        }
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
        "reason": "Limit of mapping depth [1] has been exceeded due to object field [a]"
      }
    ],
    "type": "illegal_argument_exception",
    "reason": "Limit of mapping depth [1] has been exceeded due to object field [a]"
  },
  "status": 400
}
```

### PUT /lbv-7e280f3b-nested_fields

リクエスト:

```json
{
  "settings": {
    "index.mapping.nested_fields.limit": 1
  },
  "mappings": {
    "properties": {
      "a": {
        "type": "nested"
      },
      "b": {
        "type": "nested"
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
        "reason": "Limit of nested fields [1] has been exceeded"
      }
    ],
    "type": "illegal_argument_exception",
    "reason": "Limit of nested fields [1] has been exceeded"
  },
  "status": 400
}
```

### PUT /lbv-7e280f3b-objectlimit

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0,
    "index.mapping.nested_objects.limit": 1
  },
  "mappings": {
    "properties": {
      "items": {
        "type": "nested"
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
  "index": "lbv-7e280f3b-objectlimit"
}
```

### PUT /lbv-7e280f3b-objectlimit/_doc/a

リクエスト:

```json
{
  "items": [
    {
      "v": 1
    },
    {
      "v": 2
    }
  ]
}
```

応答: HTTP 400

```json
{
  "error": {
    "root_cause": [
      {
        "type": "mapper_parsing_exception",
        "reason": "The number of nested documents has exceeded the allowed limit of [1]. This limit can be set by changing the [index.mapping.nested_objects.limit] index level setting."
      }
    ],
    "type": "mapper_parsing_exception",
    "reason": "The number of nested documents has exceeded the allowed limit of [1]. This limit can be set by changing the [index.mapping.nested_objects.limit] index level setting."
  },
  "status": 400
}
```

判定時の補足:

```json
[
  {
    "root_cause": [
      {
        "type": "illegal_argument_exception",
        "reason": "Limit of mapping depth [1] has been exceeded due to object field [a]"
      }
    ],
    "type": "illegal_argument_exception",
    "reason": "Limit of mapping depth [1] has been exceeded due to object field [a]"
  },
  {
    "root_cause": [
      {
        "type": "illegal_argument_exception",
        "reason": "Limit of nested fields [1] has been exceeded"
      }
    ],
    "type": "illegal_argument_exception",
    "reason": "Limit of nested fields [1] has been exceeded"
  },
  {
    "root_cause": [
      {
        "type": "mapper_parsing_exception",
        "reason": "The number of nested documents has exceeded the allowed limit of [1]. This limit can be set by changing the [index.mapping.nested_objects.limit] index level setting."
      }
    ],
    "type": "mapper_parsing_exception",
    "reason": "The number of nested documents has exceeded the allowed limit of [1]. This limit can be set by changing the [index.mapping.nested_objects.limit] index level setting."
  }
]
```
