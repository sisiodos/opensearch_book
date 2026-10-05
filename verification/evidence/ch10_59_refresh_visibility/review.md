# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch10_59_refresh_visibility: PASS

第10章 10.1 / 10.4 — refresh visibility and segment/flush APIs

### PUT /lbv-7e280f3b-refresh

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0,
    "refresh_interval": "-1"
  },
  "mappings": {
    "properties": {
      "v": {
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
  "index": "lbv-7e280f3b-refresh"
}
```

### PUT /lbv-7e280f3b-refresh/_doc/a

リクエスト:

```json
{
  "v": "new"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-refresh",
  "_id": "a",
  "_version": 1,
  "result": "created",
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 0,
  "_primary_term": 1
}
```

### GET /lbv-7e280f3b-refresh/_doc/a

応答: HTTP 200

```json
{
  "_index": "lbv-7e280f3b-refresh",
  "_id": "a",
  "_version": 1,
  "_seq_no": 0,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "v": "new"
  }
}
```

### POST /lbv-7e280f3b-refresh/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "match_all": {}
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
      "value": 0,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  }
}
```

### POST /lbv-7e280f3b-refresh/_refresh

応答: HTTP 200

```json
{
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  }
}
```

### POST /lbv-7e280f3b-refresh/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "match_all": {}
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
    "max_score": 1.0,
    "hits": [
      {
        "_index": "lbv-7e280f3b-refresh",
        "_id": "a",
        "_score": 1.0,
        "_source": {
          "v": "new"
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-refresh/_flush

応答: HTTP 200

```json
{
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  }
}
```

### GET /lbv-7e280f3b-refresh/_segments

応答: HTTP 200

```json
{
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "indices": {
    "lbv-7e280f3b-refresh": {
      "shards": {
        "0": [
          {
            "routing": {
              "state": "STARTED",
              "primary": true,
              "node": "p_F7jBWOQHKoSIT3TrF0ig"
            },
            "num_committed_segments": 1,
            "num_search_segments": 1,
            "segments": {
              "_0": {
                "generation": 0,
                "num_docs": 1,
                "deleted_docs": 0,
                "size_in_bytes": 3909,
                "memory_in_bytes": 0,
                "committed": true,
                "search": true,
                "version": "10.5.1",
                "compound": true,
                "attributes": {
                  "Lucene90StoredFieldsFormat.mode": "BEST_SPEED"
                }
              }
            }
          }
        ]
      }
    }
  }
}
```

判定時の補足:

```json
{
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "indices": {
    "lbv-7e280f3b-refresh": {
      "shards": {
        "0": [
          {
            "routing": {
              "state": "STARTED",
              "primary": true,
              "node": "p_F7jBWOQHKoSIT3TrF0ig"
            },
            "num_committed_segments": 1,
            "num_search_segments": 1,
            "segments": {
              "_0": {
                "generation": 0,
                "num_docs": 1,
                "deleted_docs": 0,
                "size_in_bytes": 3909,
                "memory_in_bytes": 0,
                "committed": true,
                "search": true,
                "version": "10.5.1",
                "compound": true,
                "attributes": {
                  "Lucene90StoredFieldsFormat.mode": "BEST_SPEED"
                }
              }
            }
          }
        ]
      }
    }
  }
}
```
