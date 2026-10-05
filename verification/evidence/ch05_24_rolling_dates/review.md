# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch05_24_rolling_dates: PASS

第5章 5.4 — rolling 30 days excludes future dates

### PUT /lbv-7e280f3b-rolling

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
  "index": "lbv-7e280f3b-rolling"
}
```

### PUT /lbv-7e280f3b-rolling/_doc/recent?refresh=true

リクエスト:

```json
{
  "created_at": "2026-09-28T05:56:23.697798+00:00"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-rolling",
  "_id": "recent",
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

### PUT /lbv-7e280f3b-rolling/_doc/old?refresh=true

リクエスト:

```json
{
  "created_at": "2026-09-02T05:56:23.697798+00:00"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-rolling",
  "_id": "old",
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

### PUT /lbv-7e280f3b-rolling/_doc/future?refresh=true

リクエスト:

```json
{
  "created_at": "2026-10-04T05:56:23.697798+00:00"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-rolling",
  "_id": "future",
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

### POST /lbv-7e280f3b-rolling/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "range": {
      "created_at": {
        "gte": "now-30d",
        "lte": "now"
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
        "_index": "lbv-7e280f3b-rolling",
        "_id": "recent",
        "_score": 1.0,
        "_source": {
          "created_at": "2026-09-28T05:56:23.697798+00:00"
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
