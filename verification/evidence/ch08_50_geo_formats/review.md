# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch08_50_geo_formats: PASS

第8章 8.2 — three coordinate formats give same search results

### PUT /lbv-7e280f3b-geoformats

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
  "index": "lbv-7e280f3b-geoformats"
}
```

### PUT /lbv-7e280f3b-geoformats/_doc/0?refresh=true

リクエスト:

```json
{
  "location": "35.681236,139.767125"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-geoformats",
  "_id": "0",
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

### PUT /lbv-7e280f3b-geoformats/_doc/1?refresh=true

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
  "_index": "lbv-7e280f3b-geoformats",
  "_id": "1",
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

### PUT /lbv-7e280f3b-geoformats/_doc/2?refresh=true

リクエスト:

```json
{
  "location": [
    139.767125,
    35.681236
  ]
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-geoformats",
  "_id": "2",
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

### POST /lbv-7e280f3b-geoformats/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "geo_distance": {
      "distance": "2km",
      "location": {
        "lat": 35.681236,
        "lon": 139.767125
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
      "value": 3,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "lbv-7e280f3b-geoformats",
        "_id": "0",
        "_score": 1.0,
        "_source": {
          "location": "35.681236,139.767125"
        }
      },
      {
        "_index": "lbv-7e280f3b-geoformats",
        "_id": "1",
        "_score": 1.0,
        "_source": {
          "location": {
            "lat": 35.681236,
            "lon": 139.767125
          }
        }
      },
      {
        "_index": "lbv-7e280f3b-geoformats",
        "_id": "2",
        "_score": 1.0,
        "_source": {
          "location": [
            139.767125,
            35.681236
          ]
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
