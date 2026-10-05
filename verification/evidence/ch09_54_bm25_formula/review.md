# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch09_54_bm25_formula: PASS

第9章 9.2.2 — BM25 explain agrees with book formula

### PUT /lbv-7e280f3b-bm25

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0,
    "similarity": {
      "book": {
        "type": "BM25",
        "k1": 1.2,
        "b": 0.75
      }
    }
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "whitespace",
        "similarity": "book"
      },
      "body": {
        "type": "text",
        "analyzer": "whitespace",
        "similarity": "book"
      },
      "popularity": {
        "type": "float"
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
  "index": "lbv-7e280f3b-bm25"
}
```

### PUT /lbv-7e280f3b-bm25/_doc/a?refresh=true

リクエスト:

```json
{
  "title": "lucene lucene",
  "body": "lucene lucene",
  "popularity": 4
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-bm25",
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

### PUT /lbv-7e280f3b-bm25/_doc/b?refresh=true

リクエスト:

```json
{
  "title": "lucene extra extra extra",
  "body": "lucene extra extra extra",
  "popularity": 4
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-bm25",
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

### PUT /lbv-7e280f3b-bm25/_doc/c?refresh=true

リクエスト:

```json
{
  "title": "other",
  "body": "other",
  "popularity": 4
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-bm25",
  "_id": "c",
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

### GET /lbv-7e280f3b-bm25/_explain/a

リクエスト:

```json
{
  "query": {
    "match": {
      "title": "lucene"
    }
  }
}
```

応答: HTTP 200

```json
{
  "_index": "lbv-7e280f3b-bm25",
  "_id": "a",
  "matched": true,
  "explanation": {
    "value": 0.30604887,
    "description": "weight(title:lucene in 0) [PerFieldSimilarity], result of:",
    "details": [
      {
        "value": 0.30604887,
        "description": "score(freq=2.0), computed as boost * idf * tf from:",
        "details": [
          {
            "value": 0.47000363,
            "description": "idf, computed as log(1 + (N - n + 0.5) / (n + 0.5)) from:",
            "details": [
              {
                "value": 2,
                "description": "n, number of documents containing term",
                "details": []
              },
              {
                "value": 3,
                "description": "N, total number of documents with field",
                "details": []
              }
            ]
          },
          {
            "value": 0.65116274,
            "description": "tf, computed as freq / (freq + k1 * (1 - b + b * dl / avgdl)) from:",
            "details": [
              {
                "value": 2.0,
                "description": "freq, occurrences of term within document",
                "details": []
              },
              {
                "value": 1.2,
                "description": "k1, term saturation parameter",
                "details": []
              },
              {
                "value": 0.75,
                "description": "b, length normalization parameter",
                "details": []
              },
              {
                "value": 2.0,
                "description": "dl, length of field",
                "details": []
              },
              {
                "value": 2.3333333,
                "description": "avgdl, average length of field",
                "details": []
              }
            ]
          }
        ]
      }
    ]
  }
}
```

判定時の補足:

```json
{
  "actual": 0.30604887,
  "book_formula": 0.30604887485768834,
  "explanation": {
    "value": 0.30604887,
    "description": "weight(title:lucene in 0) [PerFieldSimilarity], result of:",
    "details": [
      {
        "value": 0.30604887,
        "description": "score(freq=2.0), computed as boost * idf * tf from:",
        "details": [
          {
            "value": 0.47000363,
            "description": "idf, computed as log(1 + (N - n + 0.5) / (n + 0.5)) from:",
            "details": [
              {
                "value": 2,
                "description": "n, number of documents containing term",
                "details": []
              },
              {
                "value": 3,
                "description": "N, total number of documents with field",
                "details": []
              }
            ]
          },
          {
            "value": 0.65116274,
            "description": "tf, computed as freq / (freq + k1 * (1 - b + b * dl / avgdl)) from:",
            "details": [
              {
                "value": 2.0,
                "description": "freq, occurrences of term within document",
                "details": []
              },
              {
                "value": 1.2,
                "description": "k1, term saturation parameter",
                "details": []
              },
              {
                "value": 0.75,
                "description": "b, length normalization parameter",
                "details": []
              },
              {
                "value": 2.0,
                "description": "dl, length of field",
                "details": []
              },
              {
                "value": 2.3333333,
                "description": "avgdl, average length of field",
                "details": []
              }
            ]
          }
        ]
      }
    ]
  }
}
```
