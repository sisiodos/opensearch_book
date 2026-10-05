# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch06_35_dynamic_keys: PASS

第6章 6.1.2 — dynamic keys grow mapping; repeated values do not

### PUT /lbv-7e280f3b-dynamic

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  }
}
```

応答: HTTP 200

```json
{
  "acknowledged": true,
  "shards_acknowledged": true,
  "index": "lbv-7e280f3b-dynamic"
}
```

### PUT /lbv-7e280f3b-dynamic/_doc/a?refresh=true

リクエスト:

```json
{
  "attributes": {
    "custom_001": "a"
  }
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-dynamic",
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

### PUT /lbv-7e280f3b-dynamic/_doc/b?refresh=true

リクエスト:

```json
{
  "attributes": {
    "custom_001": "b"
  }
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-dynamic",
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

### GET /lbv-7e280f3b-dynamic/_mapping

応答: HTTP 200

```json
{
  "lbv-7e280f3b-dynamic": {
    "mappings": {
      "properties": {
        "attributes": {
          "properties": {
            "custom_001": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### PUT /lbv-7e280f3b-dynamic/_doc/c?refresh=true

リクエスト:

```json
{
  "attributes": {
    "custom_002": "c"
  }
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-dynamic",
  "_id": "c",
  "_version": 1,
  "result": "created",
  "forced_refresh": true,
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 2,
  "_primary_term": 1
}
```

### GET /lbv-7e280f3b-dynamic/_mapping

応答: HTTP 200

```json
{
  "lbv-7e280f3b-dynamic": {
    "mappings": {
      "properties": {
        "attributes": {
          "properties": {
            "custom_001": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "custom_002": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            }
          }
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
