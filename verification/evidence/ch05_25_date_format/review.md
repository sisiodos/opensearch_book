# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch05_25_date_format: PASS

第5章 5.4 — query format accepts dd/MM/yyyy

### PUT /lbv-7e280f3b-format

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "created_at": {
        "type": "date"
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
  "index": "lbv-7e280f3b-format"
}
```

### PUT /lbv-7e280f3b-format/_doc/a?refresh=true

リクエスト:

```json
{
  "created_at": "2024-12-15"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-format",
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

### POST /lbv-7e280f3b-format/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "range": {
      "created_at": {
        "gte": "01/12/2024",
        "lte": "15/01/2025",
        "format": "dd/MM/yyyy"
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
        "_index": "lbv-7e280f3b-format",
        "_id": "a",
        "_score": 1.0,
        "_source": {
          "created_at": "2024-12-15"
        }
      }
    ]
  }
}
```

判定時の補足:

```json
null
```
