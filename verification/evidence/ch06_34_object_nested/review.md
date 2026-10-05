# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch06_34_object_nested: PASS

第6章 6.1.1 / 6.2.2 — object false positive vs nested same-element match

### PUT /lbv-7e280f3b-route-object

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "segments": {
        "type": "object",
        "properties": {
          "from": {
            "type": "keyword"
          },
          "to": {
            "type": "keyword"
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
  "index": "lbv-7e280f3b-route-object"
}
```

### PUT /lbv-7e280f3b-route-object/_doc/route?refresh=true

リクエスト:

```json
{
  "segments": [
    {
      "from": "東京",
      "to": "京都"
    },
    {
      "from": "京都",
      "to": "大阪"
    }
  ]
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-route-object",
  "_id": "route",
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

### PUT /lbv-7e280f3b-route-nested

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "segments": {
        "type": "nested",
        "properties": {
          "from": {
            "type": "keyword"
          },
          "to": {
            "type": "keyword"
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
  "index": "lbv-7e280f3b-route-nested"
}
```

### PUT /lbv-7e280f3b-route-nested/_doc/route?refresh=true

リクエスト:

```json
{
  "segments": [
    {
      "from": "東京",
      "to": "京都"
    },
    {
      "from": "京都",
      "to": "大阪"
    }
  ]
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-route-nested",
  "_id": "route",
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

### POST /lbv-7e280f3b-route-object/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "segments.from": "東京"
          }
        },
        {
          "term": {
            "segments.to": "大阪"
          }
        }
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
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.0,
    "hits": [
      {
        "_index": "lbv-7e280f3b-route-object",
        "_id": "route",
        "_score": 0.0,
        "_source": {
          "segments": [
            {
              "from": "東京",
              "to": "京都"
            },
            {
              "from": "京都",
              "to": "大阪"
            }
          ]
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-route-nested/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "nested": {
      "path": "segments",
      "query": {
        "bool": {
          "filter": [
            {
              "term": {
                "segments.from": "東京"
              }
            },
            {
              "term": {
                "segments.to": "大阪"
              }
            }
          ]
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
      "value": 0,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  }
}
```

### POST /lbv-7e280f3b-route-nested/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "nested": {
      "path": "segments",
      "query": {
        "bool": {
          "filter": [
            {
              "term": {
                "segments.from": "東京"
              }
            },
            {
              "term": {
                "segments.to": "京都"
              }
            }
          ]
        }
      }
    }
  }
}
```

応答: HTTP 200

```json
{
  "took": 0,
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
    "max_score": 0.0,
    "hits": [
      {
        "_index": "lbv-7e280f3b-route-nested",
        "_id": "route",
        "_score": 0.0,
        "_source": {
          "segments": [
            {
              "from": "東京",
              "to": "京都"
            },
            {
              "from": "京都",
              "to": "大阪"
            }
          ]
        }
      }
    ]
  }
}
```

### GET /lbv-7e280f3b-route-object/_doc/route

応答: HTTP 200

```json
{
  "_index": "lbv-7e280f3b-route-object",
  "_id": "route",
  "_version": 1,
  "_seq_no": 0,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "segments": [
      {
        "from": "東京",
        "to": "京都"
      },
      {
        "from": "京都",
        "to": "大阪"
      }
    ]
  }
}
```

判定時の補足:

```json
null
```
