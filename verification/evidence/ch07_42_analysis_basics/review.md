# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch07_42_analysis_basics: PASS

第7章 7.1–7.2 — standard analyzer vs tokenizer vs keyword

### POST /_analyze

リクエスト:

```json
{
  "analyzer": "standard",
  "text": "OpenSearch Lucene"
}
```

応答: HTTP 200

```json
{
  "tokens": [
    {
      "token": "opensearch",
      "start_offset": 0,
      "end_offset": 10,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "lucene",
      "start_offset": 11,
      "end_offset": 17,
      "type": "<ALPHANUM>",
      "position": 1
    }
  ]
}
```

### POST /_analyze

リクエスト:

```json
{
  "tokenizer": "standard",
  "text": "OpenSearch Lucene"
}
```

応答: HTTP 200

```json
{
  "tokens": [
    {
      "token": "OpenSearch",
      "start_offset": 0,
      "end_offset": 10,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "Lucene",
      "start_offset": 11,
      "end_offset": 17,
      "type": "<ALPHANUM>",
      "position": 1
    }
  ]
}
```

### POST /_analyze

リクエスト:

```json
{
  "analyzer": "keyword",
  "text": "OpenSearch Lucene"
}
```

応答: HTTP 200

```json
{
  "tokens": [
    {
      "token": "OpenSearch Lucene",
      "start_offset": 0,
      "end_offset": 17,
      "type": "word",
      "position": 0
    }
  ]
}
```

判定時の補足:

```json
{
  "standard_analyzer": [
    "opensearch",
    "lucene"
  ],
  "standard_tokenizer": [
    "OpenSearch",
    "Lucene"
  ],
  "keyword": [
    "OpenSearch Lucene"
  ]
}
```
