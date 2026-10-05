# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch03_17_disabled_object: PASS

第3章 3.3 / 3.5 — enabled false retains arbitrary object

### PUT /lbv-7e280f3b-disabled

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "raw_payload": {
        "type": "object",
        "enabled": false
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
  "index": "lbv-7e280f3b-disabled"
}
```

### PUT /lbv-7e280f3b-disabled/_doc/a?refresh=true

リクエスト:

```json
{
  "raw_payload": {
    "deep": {
      "v": [
        1,
        "two",
        {
          "x": true
        }
      ]
    }
  }
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-disabled",
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

### GET /lbv-7e280f3b-disabled/_doc/a

応答: HTTP 200

```json
{
  "_index": "lbv-7e280f3b-disabled",
  "_id": "a",
  "_version": 1,
  "_seq_no": 0,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "raw_payload": {
      "deep": {
        "v": [
          1,
          "two",
          {
            "x": true
          }
        ]
      }
    }
  }
}
```

### GET /lbv-7e280f3b-disabled/_mapping

応答: HTTP 200

```json
{
  "lbv-7e280f3b-disabled": {
    "mappings": {
      "properties": {
        "raw_payload": {
          "type": "object",
          "enabled": false
        }
      }
    }
  }
}
```

判定時の補足:

```json
null
```
