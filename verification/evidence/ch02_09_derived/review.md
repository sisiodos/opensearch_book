# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch02_09_derived: PASS

第2章 2.3.3 — derived source reconstructs keyword array

### PUT /lbv-7e280f3b-derived

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0,
    "index.derived_source.enabled": true
  },
  "mappings": {
    "properties": {
      "tags": {
        "type": "keyword"
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
  "index": "lbv-7e280f3b-derived"
}
```

### PUT /lbv-7e280f3b-derived/_doc/a?refresh=true

リクエスト:

```json
{
  "tags": [
    "z",
    "a",
    "a"
  ]
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-derived",
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

### GET /lbv-7e280f3b-derived/_doc/a

応答: HTTP 200

```json
{
  "_index": "lbv-7e280f3b-derived",
  "_id": "a",
  "_version": 1,
  "_seq_no": 0,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "tags": [
      "a",
      "z"
    ]
  }
}
```

判定時の補足:

```json
{
  "input": [
    "z",
    "a",
    "a"
  ],
  "reconstructed": {
    "tags": [
      "a",
      "z"
    ]
  }
}
```
