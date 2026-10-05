# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch02_06_date_nanos: PASS

第2章 2.2.5 — date_nanos retains fractional precision

### PUT /lbv-7e280f3b-nanos

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "time": {
        "type": "date_nanos"
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
  "index": "lbv-7e280f3b-nanos"
}
```

### PUT /lbv-7e280f3b-nanos/_doc/n?refresh=true

リクエスト:

```json
{
  "time": "2024-05-01T00:00:00.123456789Z"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-nanos",
  "_id": "n",
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

### POST /lbv-7e280f3b-nanos/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "match_all": {}
  },
  "fields": [
    {
      "field": "time",
      "format": "strict_date_optional_time_nanos"
    }
  ],
  "_source": false
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
        "_index": "lbv-7e280f3b-nanos",
        "_id": "n",
        "_score": 1.0,
        "fields": {
          "time": [
            "2024-05-01T00:00:00.123456789Z"
          ]
        }
      }
    ]
  }
}
```

判定時の補足:

```json
{
  "time": [
    "2024-05-01T00:00:00.123456789Z"
  ]
}
```
