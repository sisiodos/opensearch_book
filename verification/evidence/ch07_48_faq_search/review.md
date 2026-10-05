# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch07_48_faq_search: PASS

第7章 7.4.5 — faq_query multi-word synonym graph

### PUT /lbv-7e280f3b-faq

リクエスト:

```json
{
  "settings": {
    "analysis": {
      "filter": {
        "synonym_filter_expanded": {
          "type": "synonym_graph",
          "synonyms": [
            "pc, personal computer"
          ]
        }
      },
      "analyzer": {
        "faq_query": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "synonym_filter_expanded"
          ]
        }
      }
    },
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "body": {
        "type": "text",
        "analyzer": "standard",
        "search_analyzer": "faq_query"
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
  "index": "lbv-7e280f3b-faq"
}
```

### PUT /lbv-7e280f3b-faq/_doc/a?refresh=true

リクエスト:

```json
{
  "body": "personal computer"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-faq",
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

### PUT /lbv-7e280f3b-faq/_doc/b?refresh=true

リクエスト:

```json
{
  "body": "pc"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-faq",
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

### POST /lbv-7e280f3b-faq/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "match": {
      "body": "PC"
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
      "value": 2,
      "relation": "eq"
    },
    "max_score": 0.5545178,
    "hits": [
      {
        "_index": "lbv-7e280f3b-faq",
        "_id": "a",
        "_score": 0.5545178,
        "_source": {
          "body": "personal computer"
        }
      },
      {
        "_index": "lbv-7e280f3b-faq",
        "_id": "b",
        "_score": 0.3648143,
        "_source": {
          "body": "pc"
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-faq/_analyze

リクエスト:

```json
{
  "analyzer": "faq_query",
  "text": "PC"
}
```

応答: HTTP 200

```json
{
  "tokens": [
    {
      "token": "personal",
      "start_offset": 0,
      "end_offset": 2,
      "type": "SYNONYM",
      "position": 0
    },
    {
      "token": "pc",
      "start_offset": 0,
      "end_offset": 2,
      "type": "<ALPHANUM>",
      "position": 0,
      "positionLength": 2
    },
    {
      "token": "computer",
      "start_offset": 0,
      "end_offset": 2,
      "type": "SYNONYM",
      "position": 1
    }
  ]
}
```

判定時の補足:

```json
[
  {
    "token": "personal",
    "start_offset": 0,
    "end_offset": 2,
    "type": "SYNONYM",
    "position": 0
  },
  {
    "token": "pc",
    "start_offset": 0,
    "end_offset": 2,
    "type": "<ALPHANUM>",
    "position": 0,
    "positionLength": 2
  },
  {
    "token": "computer",
    "start_offset": 0,
    "end_offset": 2,
    "type": "SYNONYM",
    "position": 1
  }
]
```
