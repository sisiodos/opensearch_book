# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch06_39_nested_count: PASS

第6章 6.2.5 — 100 nested objects produce 101 Lucene documents

### PUT /lbv-7e280f3b-nestedcount

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
  "index": "lbv-7e280f3b-nestedcount"
}
```

### PUT /lbv-7e280f3b-nestedcount/_doc/a?refresh=true

リクエスト:

```json
{
  "items": [
    {
      "v": 0
    },
    {
      "v": 1
    },
    {
      "v": 2
    },
    {
      "v": 3
    },
    {
      "v": 4
    },
    {
      "v": 5
    },
    {
      "v": 6
    },
    {
      "v": 7
    },
    {
      "v": 8
    },
    {
      "v": 9
    },
    {
      "v": 10
    },
    {
      "v": 11
    },
    {
      "v": 12
    },
    {
      "v": 13
    },
    {
      "v": 14
    },
    {
      "v": 15
    },
    {
      "v": 16
    },
    {
      "v": 17
    },
    {
      "v": 18
    },
    {
      "v": 19
    },
    {
      "v": 20
    },
    {
      "v": 21
    },
    {
      "v": 22
    },
    {
      "v": 23
    },
    {
      "v": 24
    },
    {
      "v": 25
    },
    {
      "v": 26
    },
    {
      "v": 27
    },
    {
      "v": 28
    },
    {
      "v": 29
    },
    {
      "v": 30
    },
    {
      "v": 31
    },
    {
      "v": 32
    },
    {
      "v": 33
    },
    {
      "v": 34
    },
    {
      "v": 35
    },
    {
      "v": 36
    },
    {
      "v": 37
    },
    {
      "v": 38
    },
    {
      "v": 39
    },
    {
      "v": 40
    },
    {
      "v": 41
    },
    {
      "v": 42
    },
    {
      "v": 43
    },
    {
      "v": 44
    },
    {
      "v": 45
    },
    {
      "v": 46
    },
    {
      "v": 47
    },
    {
      "v": 48
    },
    {
      "v": 49
    },
    {
      "v": 50
    },
    {
      "v": 51
    },
    {
      "v": 52
    },
    {
      "v": 53
    },
    {
      "v": 54
    },
    {
      "v": 55
    },
    {
      "v": 56
    },
    {
      "v": 57
    },
    {
      "v": 58
    },
    {
      "v": 59
    },
    {
      "v": 60
    },
    {
      "v": 61
    },
    {
      "v": 62
    },
    {
      "v": 63
    },
    {
      "v": 64
    },
    {
      "v": 65
    },
    {
      "v": 66
    },
    {
      "v": 67
    },
    {
      "v": 68
    },
    {
      "v": 69
    },
    {
      "v": 70
    },
    {
      "v": 71
    },
    {
      "v": 72
    },
    {
      "v": 73
    },
    {
      "v": 74
    },
    {
      "v": 75
    },
    {
      "v": 76
    },
    {
      "v": 77
    },
    {
      "v": 78
    },
    {
      "v": 79
    },
    {
      "v": 80
    },
    {
      "v": 81
    },
    {
      "v": 82
    },
    {
      "v": 83
    },
    {
      "v": 84
    },
    {
      "v": 85
    },
    {
      "v": 86
    },
    {
      "v": 87
    },
    {
      "v": 88
    },
    {
      "v": 89
    },
    {
      "v": 90
    },
    {
      "v": 91
    },
    {
      "v": 92
    },
    {
      "v": 93
    },
    {
      "v": 94
    },
    {
      "v": 95
    },
    {
      "v": 96
    },
    {
      "v": 97
    },
    {
      "v": 98
    },
    {
      "v": 99
    }
  ]
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-nestedcount",
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

### POST /lbv-7e280f3b-nestedcount/_flush

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

### GET /lbv-7e280f3b-nestedcount/_stats/docs

応答: HTTP 200

```json
{
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "_all": {
    "primaries": {
      "docs": {
        "count": 101,
        "deleted": 0
      }
    },
    "total": {
      "docs": {
        "count": 101,
        "deleted": 0
      }
    }
  },
  "indices": {
    "lbv-7e280f3b-nestedcount": {
      "uuid": "NPmciPyNS7-3uivAyV_6mA",
      "primaries": {
        "docs": {
          "count": 101,
          "deleted": 0
        }
      },
      "total": {
        "docs": {
          "count": 101,
          "deleted": 0
        }
      }
    }
  }
}
```

### POST /lbv-7e280f3b-nestedcount/_search

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
        "_index": "lbv-7e280f3b-nestedcount",
        "_id": "a",
        "_score": 1.0,
        "_source": {
          "items": [
            {
              "v": 0
            },
            {
              "v": 1
            },
            {
              "v": 2
            },
            {
              "v": 3
            },
            {
              "v": 4
            },
            {
              "v": 5
            },
            {
              "v": 6
            },
            {
              "v": 7
            },
            {
              "v": 8
            },
            {
              "v": 9
            },
            {
              "v": 10
            },
            {
              "v": 11
            },
            {
              "v": 12
            },
            {
              "v": 13
            },
            {
              "v": 14
            },
            {
              "v": 15
            },
            {
              "v": 16
            },
            {
              "v": 17
            },
            {
              "v": 18
            },
            {
              "v": 19
            },
            {
              "v": 20
            },
            {
              "v": 21
            },
            {
              "v": 22
            },
            {
              "v": 23
            },
            {
              "v": 24
            },
            {
              "v": 25
            },
            {
              "v": 26
            },
            {
              "v": 27
            },
            {
              "v": 28
            },
            {
              "v": 29
            },
            {
              "v": 30
            },
            {
              "v": 31
            },
            {
              "v": 32
            },
            {
              "v": 33
            },
            {
              "v": 34
            },
            {
              "v": 35
            },
            {
              "v": 36
            },
            {
              "v": 37
            },
            {
              "v": 38
            },
            {
              "v": 39
            },
            {
              "v": 40
            },
            {
              "v": 41
            },
            {
              "v": 42
            },
            {
              "v": 43
            },
            {
              "v": 44
            },
            {
              "v": 45
            },
            {
              "v": 46
            },
            {
              "v": 47
            },
            {
              "v": 48
            },
            {
              "v": 49
            },
            {
              "v": 50
            },
            {
              "v": 51
            },
            {
              "v": 52
            },
            {
              "v": 53
            },
            {
              "v": 54
            },
            {
              "v": 55
            },
            {
              "v": 56
            },
            {
              "v": 57
            },
            {
              "v": 58
            },
            {
              "v": 59
            },
            {
              "v": 60
            },
            {
              "v": 61
            },
            {
              "v": 62
            },
            {
              "v": 63
            },
            {
              "v": 64
            },
            {
              "v": 65
            },
            {
              "v": 66
            },
            {
              "v": 67
            },
            {
              "v": 68
            },
            {
              "v": 69
            },
            {
              "v": 70
            },
            {
              "v": 71
            },
            {
              "v": 72
            },
            {
              "v": 73
            },
            {
              "v": 74
            },
            {
              "v": 75
            },
            {
              "v": 76
            },
            {
              "v": 77
            },
            {
              "v": 78
            },
            {
              "v": 79
            },
            {
              "v": 80
            },
            {
              "v": 81
            },
            {
              "v": 82
            },
            {
              "v": 83
            },
            {
              "v": 84
            },
            {
              "v": 85
            },
            {
              "v": 86
            },
            {
              "v": 87
            },
            {
              "v": 88
            },
            {
              "v": 89
            },
            {
              "v": 90
            },
            {
              "v": 91
            },
            {
              "v": 92
            },
            {
              "v": 93
            },
            {
              "v": 94
            },
            {
              "v": 95
            },
            {
              "v": 96
            },
            {
              "v": 97
            },
            {
              "v": 98
            },
            {
              "v": 99
            }
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
  "lucene_documents": 101,
  "search_documents": 1
}
```
