# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch07_47_natural_search: PASS

第7章 7.4.3 — natural_search definition and explicit Japanese stopwords

### PUT /lbv-7e280f3b-natural

リクエスト:

```json
{
  "settings": {
    "analysis": {
      "filter": {
        "ja_stop": {
          "type": "stop",
          "stopwords": [
            "が",
            "は",
            "の"
          ]
        },
        "synonym_filter": {
          "type": "synonym_graph",
          "synonyms": [
            "pc, パソコン"
          ]
        }
      },
      "analyzer": {
        "natural_search": {
          "type": "custom",
          "tokenizer": "kuromoji_tokenizer",
          "filter": [
            "kuromoji_baseform",
            "kuromoji_part_of_speech",
            "lowercase",
            "ja_stop",
            "synonym_filter"
          ]
        },
        "custom_ja": {
          "type": "custom",
          "tokenizer": "kuromoji_tokenizer",
          "filter": [
            "kuromoji_baseform",
            "kuromoji_part_of_speech",
            "lowercase"
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
        "search_analyzer": "natural_search"
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
  "index": "lbv-7e280f3b-natural"
}
```

### PUT /lbv-7e280f3b-natural/_doc/a?refresh=true

リクエスト:

```json
{
  "description": "安いパソコン"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-natural",
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

### POST /lbv-7e280f3b-natural/_search

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
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.13076457,
    "hits": [
      {
        "_index": "lbv-7e280f3b-natural",
        "_id": "a",
        "_score": 0.13076457,
        "_source": {
          "description": "安いパソコン"
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-natural/_analyze

リクエスト:

```json
{
  "analyzer": "natural_search",
  "text": "パソコンが安い"
}
```

応答: HTTP 200

```json
{
  "tokens": [
    {
      "token": "pc",
      "start_offset": 0,
      "end_offset": 4,
      "type": "SYNONYM",
      "position": 0
    },
    {
      "token": "パソコン",
      "start_offset": 0,
      "end_offset": 4,
      "type": "word",
      "position": 0
    },
    {
      "token": "安い",
      "start_offset": 5,
      "end_offset": 7,
      "type": "word",
      "position": 2
    }
  ]
}
```

判定時の補足:

```json
[
  {
    "token": "pc",
    "start_offset": 0,
    "end_offset": 4,
    "type": "SYNONYM",
    "position": 0
  },
  {
    "token": "パソコン",
    "start_offset": 0,
    "end_offset": 4,
    "type": "word",
    "position": 0
  },
  {
    "token": "安い",
    "start_offset": 5,
    "end_offset": 7,
    "type": "word",
    "position": 2
  }
]
```
