# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch02_03_term_match: PASS

第2章 2.1.1 / 2.1.4 — term is raw; match analyzes text

### POST /lbv-7e280f3b-basic/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "term": {
      "name": "Lucene"
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

### POST /lbv-7e280f3b-basic/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "match": {
      "name": "Lucene"
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
      "value": 2,
      "relation": "eq"
    },
    "max_score": 0.06069608,
    "hits": [
      {
        "_index": "lbv-7e280f3b-basic",
        "_id": "b",
        "_score": 0.06069608,
        "_source": {
          "name": "Lucene reference",
          "code": "DEF456",
          "price": 20,
          "date": "2024-05-02",
          "flag": false,
          "tags": [
            "green"
          ],
          "display": "other",
          "location": {
            "lat": 35.7,
            "lon": 139.73
          }
        }
      },
      {
        "_index": "lbv-7e280f3b-basic",
        "_id": "a",
        "_score": 0.06069608,
        "_source": {
          "name": "OpenSearch Lucene",
          "code": "ABC123",
          "price": 100,
          "date": "2024-05-01",
          "flag": true,
          "tags": [
            "red",
            "blue"
          ],
          "display": "original",
          "location": {
            "lat": 35.681236,
            "lon": 139.767125
          }
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-basic/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "term": {
      "code": "ABC"
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

### POST /lbv-7e280f3b-basic/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "term": {
      "code": "ABC123"
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
    "max_score": 1.0,
    "hits": [
      {
        "_index": "lbv-7e280f3b-basic",
        "_id": "a",
        "_score": 1.0,
        "_source": {
          "name": "OpenSearch Lucene",
          "code": "ABC123",
          "price": 100,
          "date": "2024-05-01",
          "flag": true,
          "tags": [
            "red",
            "blue"
          ],
          "display": "original",
          "location": {
            "lat": 35.681236,
            "lon": 139.767125
          }
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
