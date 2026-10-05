# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch07_46_custom_ja: PASS

第7章 7.3.3 — complete custom_ja book mapping and search synonyms

### PUT /lbv-7e280f3b-customja

リクエスト:

```json
{
  "settings": {
    "analysis": {
      "filter": {
        "synonym_filter": {
          "type": "synonym_graph",
          "synonyms": [
            "pc, パソコン, コンピューター"
          ]
        }
      },
      "analyzer": {
        "custom_ja": {
          "type": "custom",
          "tokenizer": "kuromoji_tokenizer",
          "filter": [
            "kuromoji_baseform",
            "kuromoji_part_of_speech",
            "lowercase"
          ]
        },
        "custom_ja_search": {
          "type": "custom",
          "tokenizer": "kuromoji_tokenizer",
          "filter": [
            "kuromoji_baseform",
            "kuromoji_part_of_speech",
            "lowercase",
            "synonym_filter"
          ]
        }
      }
    },
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "description": {
        "type": "text",
        "analyzer": "custom_ja",
        "search_analyzer": "custom_ja_search"
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
  "index": "lbv-7e280f3b-customja"
}
```

### PUT /lbv-7e280f3b-customja/_doc/a?refresh=true

リクエスト:

```json
{
  "description": "パソコン"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-customja",
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

### PUT /lbv-7e280f3b-customja/_doc/b?refresh=true

リクエスト:

```json
{
  "description": "PC"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-customja",
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

### POST /lbv-7e280f3b-customja/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "match": {
      "description": "PC"
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
    "max_score": 0.31506687,
    "hits": [
      {
        "_index": "lbv-7e280f3b-customja",
        "_id": "a",
        "_score": 0.31506687,
        "_source": {
          "description": "パソコン"
        }
      },
      {
        "_index": "lbv-7e280f3b-customja",
        "_id": "b",
        "_score": 0.31506687,
        "_source": {
          "description": "PC"
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-customja/_analyze

リクエスト:

```json
{
  "analyzer": "custom_ja",
  "text": "PC"
}
```

応答: HTTP 200

```json
{
  "tokens": [
    {
      "token": "pc",
      "start_offset": 0,
      "end_offset": 2,
      "type": "word",
      "position": 0
    }
  ]
}
```

### POST /lbv-7e280f3b-customja/_analyze

リクエスト:

```json
{
  "analyzer": "custom_ja_search",
  "text": "PC"
}
```

応答: HTTP 200

```json
{
  "tokens": [
    {
      "token": "パソコン",
      "start_offset": 0,
      "end_offset": 2,
      "type": "SYNONYM",
      "position": 0
    },
    {
      "token": "コンピューター",
      "start_offset": 0,
      "end_offset": 2,
      "type": "SYNONYM",
      "position": 0
    },
    {
      "token": "pc",
      "start_offset": 0,
      "end_offset": 2,
      "type": "word",
      "position": 0
    }
  ]
}
```

判定時の補足:

```json
{
  "index_tokens": [
    {
      "token": "pc",
      "start_offset": 0,
      "end_offset": 2,
      "type": "word",
      "position": 0
    }
  ],
  "search_tokens": [
    {
      "token": "パソコン",
      "start_offset": 0,
      "end_offset": 2,
      "type": "SYNONYM",
      "position": 0
    },
    {
      "token": "コンピューター",
      "start_offset": 0,
      "end_offset": 2,
      "type": "SYNONYM",
      "position": 0
    },
    {
      "token": "pc",
      "start_offset": 0,
      "end_offset": 2,
      "type": "word",
      "position": 0
    }
  ]
}
```
