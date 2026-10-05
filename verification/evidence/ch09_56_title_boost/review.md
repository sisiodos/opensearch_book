# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch09_56_title_boost: PASS

第9章 9.3.2 — title boost raises title match

### PUT /lbv-7e280f3b-boost

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text"
      },
      "body": {
        "type": "text"
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
  "index": "lbv-7e280f3b-boost"
}
```

### PUT /lbv-7e280f3b-boost/_doc/title?refresh=true

リクエスト:

```json
{
  "title": "OpenSearch",
  "body": "other"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-boost",
  "_id": "title",
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

### PUT /lbv-7e280f3b-boost/_doc/body?refresh=true

リクエスト:

```json
{
  "title": "other",
  "body": "OpenSearch"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-boost",
  "_id": "body",
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

### POST /lbv-7e280f3b-boost/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "multi_match": {
      "query": "OpenSearch",
      "fields": [
        "title^3",
        "body"
      ]
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
      "value": 2,
      "relation": "eq"
    },
    "max_score": 0.9452007,
    "hits": [
      {
        "_index": "lbv-7e280f3b-boost",
        "_id": "title",
        "_score": 0.9452007,
        "_source": {
          "title": "OpenSearch",
          "body": "other"
        }
      },
      {
        "_index": "lbv-7e280f3b-boost",
        "_id": "body",
        "_score": 0.31506687,
        "_source": {
          "title": "other",
          "body": "OpenSearch"
        }
      }
    ]
  }
}
```

判定時の補足:

```json
{
  "title": 0.9452007,
  "body": 0.31506687
}
```
