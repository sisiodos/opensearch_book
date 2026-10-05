# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch01_01_replace_id: PASS

第1章 1.1 — same _id replaces one document

### GET /lbv-7e280f3b-basic/_doc/a

応答: HTTP 200

```json
{
  "_index": "lbv-7e280f3b-basic",
  "_id": "a",
  "_version": 1,
  "_seq_no": 0,
  "_primary_term": 1,
  "found": true,
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
```

### PUT /lbv-7e280f3b-basic/_doc/a?refresh=true

リクエスト:

```json
{
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
```

応答: HTTP 200

```json
{
  "_index": "lbv-7e280f3b-basic",
  "_id": "a",
  "_version": 2,
  "result": "updated",
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

### GET /lbv-7e280f3b-basic/_count

応答: HTTP 200

```json
{
  "count": 2,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  }
}
```

判定時の補足:

```json
{
  "documents": 2,
  "id": "a"
}
```
