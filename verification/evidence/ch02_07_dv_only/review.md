# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch02_07_dv_only: PASS

第2章 2.3.4 — DocValues-only range, aggregate and sort

### PUT /lbv-7e280f3b-dvonly

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
        "index": false
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
  "index": "lbv-7e280f3b-dvonly"
}
```

### PUT /lbv-7e280f3b-dvonly/_doc/a?refresh=true

リクエスト:

```json
{
  "v": 2
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-dvonly",
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

### PUT /lbv-7e280f3b-dvonly/_doc/b?refresh=true

リクエスト:

```json
{
  "v": 8
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-dvonly",
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

### POST /lbv-7e280f3b-dvonly/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "range": {
      "v": {
        "gte": 5
      }
    }
  },
  "sort": [
    {
      "v": "desc"
    }
  ],
  "aggs": {
    "avg": {
      "avg": {
        "field": "v"
      }
    }
  }
}
```

応答: HTTP 200

```json
{
  "took": 2,
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
    "max_score": null,
    "hits": [
      {
        "_index": "lbv-7e280f3b-dvonly",
        "_id": "b",
        "_score": null,
        "_source": {
          "v": 8
        },
        "sort": [
          8
        ]
      }
    ]
  },
  "aggregations": {
    "avg": {
      "value": 8.0
    }
  }
}
```

判定時の補足:

```json
null
```
