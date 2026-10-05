# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch08_52_geo_rank: PASS

第8章 8.4 — distance sort and gauss decay at scale

### PUT /lbv-7e280f3b-georank

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "location": {
        "type": "geo_point"
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
  "index": "lbv-7e280f3b-georank"
}
```

### PUT /lbv-7e280f3b-georank/_doc/station?refresh=true

リクエスト:

```json
{
  "location": {
    "lat": 35.681236,
    "lon": 139.767125
  }
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-georank",
  "_id": "station",
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

### PUT /lbv-7e280f3b-georank/_doc/west?refresh=true

リクエスト:

```json
{
  "location": {
    "lat": 35.6895,
    "lon": 139.72
  }
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-georank",
  "_id": "west",
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

### PUT /lbv-7e280f3b-georank/_doc/far?refresh=true

リクエスト:

```json
{
  "location": {
    "lat": 34.6937,
    "lon": 135.5023
  }
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-georank",
  "_id": "far",
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

### POST /lbv-7e280f3b-georank/_search

リクエスト:

```json
{
  "query": {
    "match_all": {}
  },
  "sort": [
    {
      "_geo_distance": {
        "location": {
          "lat": 35.681236,
          "lon": 139.767125
        },
        "order": "asc",
        "unit": "km"
      }
    }
  ]
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
      "value": 3,
      "relation": "eq"
    },
    "max_score": null,
    "hits": [
      {
        "_index": "lbv-7e280f3b-georank",
        "_id": "station",
        "_score": null,
        "_source": {
          "location": {
            "lat": 35.681236,
            "lon": 139.767125
          }
        },
        "sort": [
          0.0
        ]
      },
      {
        "_index": "lbv-7e280f3b-georank",
        "_id": "west",
        "_score": null,
        "_source": {
          "location": {
            "lat": 35.6895,
            "lon": 139.72
          }
        },
        "sort": [
          4.354224861422175
        ]
      },
      {
        "_index": "lbv-7e280f3b-georank",
        "_id": "far",
        "_score": null,
        "_source": {
          "location": {
            "lat": 34.6937,
            "lon": 135.5023
          }
        },
        "sort": [
          402.78793393126426
        ]
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-georank/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "function_score": {
      "query": {
        "match_all": {}
      },
      "functions": [
        {
          "gauss": {
            "location": {
              "origin": "35.681236,139.767125",
              "scale": "1km"
            }
          }
        }
      ],
      "score_mode": "multiply",
      "boost_mode": "multiply"
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
      "value": 3,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "lbv-7e280f3b-georank",
        "_id": "station",
        "_score": 1.0,
        "_source": {
          "location": {
            "lat": 35.681236,
            "lon": 139.767125
          }
        }
      },
      {
        "_index": "lbv-7e280f3b-georank",
        "_id": "west",
        "_score": 1.9619583e-06,
        "_source": {
          "location": {
            "lat": 35.6895,
            "lon": 139.72
          }
        }
      },
      {
        "_index": "lbv-7e280f3b-georank",
        "_id": "far",
        "_score": 0.0,
        "_source": {
          "location": {
            "lat": 34.6937,
            "lon": 135.5023
          }
        }
      }
    ]
  }
}
```

### PUT /lbv-7e280f3b-georank/_doc/scale?refresh=true

リクエスト:

```json
{
  "location": {
    "lat": 35.69022920365613,
    "lon": 139.767125
  }
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-georank",
  "_id": "scale",
  "_version": 1,
  "result": "created",
  "forced_refresh": true,
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 3,
  "_primary_term": 1
}
```

### POST /lbv-7e280f3b-georank/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "function_score": {
      "query": {
        "match_all": {}
      },
      "functions": [
        {
          "gauss": {
            "location": {
              "origin": "35.681236,139.767125",
              "scale": "1km"
            }
          }
        }
      ],
      "score_mode": "multiply",
      "boost_mode": "multiply"
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
      "value": 4,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "lbv-7e280f3b-georank",
        "_id": "station",
        "_score": 1.0,
        "_source": {
          "location": {
            "lat": 35.681236,
            "lon": 139.767125
          }
        }
      },
      {
        "_index": "lbv-7e280f3b-georank",
        "_id": "scale",
        "_score": 0.5000003,
        "_source": {
          "location": {
            "lat": 35.69022920365613,
            "lon": 139.767125
          }
        }
      },
      {
        "_index": "lbv-7e280f3b-georank",
        "_id": "west",
        "_score": 1.9619583e-06,
        "_source": {
          "location": {
            "lat": 35.6895,
            "lon": 139.72
          }
        }
      },
      {
        "_index": "lbv-7e280f3b-georank",
        "_id": "far",
        "_score": 0.0,
        "_source": {
          "location": {
            "lat": 34.6937,
            "lon": 135.5023
          }
        }
      }
    ]
  }
}
```

判定時の補足:

```json
{
  "at_center": 1.0,
  "approximately_1km": 0.5000003
}
```
