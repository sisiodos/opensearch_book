# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch06_40_nestedagg: PASS

第6章 6.2.5 — nested aggregation counts child scope

### PUT /lbv-7e280f3b-nestedagg

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "items": {
        "type": "nested",
        "properties": {
          "v": {
            "type": "integer"
          }
        }
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
  "index": "lbv-7e280f3b-nestedagg"
}
```

### PUT /lbv-7e280f3b-nestedagg/_doc/a?refresh=true

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

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-nestedagg",
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

### POST /lbv-7e280f3b-nestedagg/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "match_all": {}
  },
  "aggs": {
    "items": {
      "nested": {
        "path": "items"
      },
      "aggs": {
        "avg": {
          "avg": {
            "field": "items.v"
          }
        }
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
        "_index": "lbv-7e280f3b-nestedagg",
        "_id": "a",
        "_score": 1.0,
        "_source": {
          "items": [
            {
              "v": 1
            },
            {
              "v": 2
            }
          ]
        }
      }
    ]
  },
  "aggregations": {
    "items": {
      "doc_count": 2,
      "avg": {
        "value": 1.5
      }
    }
  }
}
```

判定時の補足:

```json
{
  "doc_count": 2,
  "avg": {
    "value": 1.5
  }
}
```
