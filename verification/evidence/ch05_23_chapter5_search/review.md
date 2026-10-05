# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch05_23_chapter5_search: PASS

第5章 5.2–5.7 — book exact/prefix/match/phrase/range/terms/AND/sort examples

### PUT /lbv-7e280f3b-products

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0,
    "analysis": {
      "analyzer": {
        "ja": {
          "type": "custom",
          "tokenizer": "book_ja",
          "filter": [
            "lowercase"
          ]
        }
      },
      "tokenizer": {
        "book_ja": {
          "type": "kuromoji_tokenizer",
          "user_dictionary_rules": [
            "ワイヤレスイヤホン,ワイヤレス イヤホン,ワイヤレス イヤホン,カスタム名詞",
            "ワイヤレススピーカー,ワイヤレス スピーカー,ワイヤレス スピーカー,カスタム名詞",
            "イヤホン,イヤホン,イヤホン,カスタム名詞"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "product_id": {
        "type": "keyword"
      },
      "status": {
        "type": "keyword"
      },
      "category_code": {
        "type": "keyword"
      },
      "categories": {
        "type": "keyword"
      },
      "product_name": {
        "type": "text",
        "analyzer": "ja",
        "fields": {
          "keyword": {
            "type": "keyword"
          }
        }
      },
      "price": {
        "type": "integer"
      },
      "created_at": {
        "type": "date"
      },
      "release_date": {
        "type": "date"
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
  "index": "lbv-7e280f3b-products"
}
```

### PUT /lbv-7e280f3b-products/_doc/ABC123?refresh=true

リクエスト:

```json
{
  "product_id": "ABC123",
  "status": "available",
  "product_name": "ワイヤレスイヤホン",
  "price": 2000,
  "created_at": "2024-12-15",
  "release_date": "2024-12-15",
  "category_code": "AUDIO",
  "categories": [
    "アウトドア",
    "防水"
  ]
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-products",
  "_id": "ABC123",
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

### PUT /lbv-7e280f3b-products/_doc/B?refresh=true

リクエスト:

```json
{
  "product_id": "B",
  "status": "available",
  "product_name": "イヤホン",
  "price": 6000,
  "created_at": "2024-12-15",
  "release_date": "2024-12-15",
  "category_code": "AUDIO",
  "categories": [
    "アウトドア"
  ]
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-products",
  "_id": "B",
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

### PUT /lbv-7e280f3b-products/_doc/C?refresh=true

リクエスト:

```json
{
  "product_id": "C",
  "status": "available",
  "product_name": "ワイヤレススピーカー",
  "price": 500,
  "created_at": "2024-12-15",
  "release_date": "2024-12-15",
  "category_code": "ELEC",
  "categories": [
    "アウトドア"
  ]
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-products",
  "_id": "C",
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

### POST /lbv-7e280f3b-products/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "term": {
      "product_id": "ABC123"
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
    "max_score": 1.0,
    "hits": [
      {
        "_index": "lbv-7e280f3b-products",
        "_id": "ABC123",
        "_score": 1.0,
        "_source": {
          "product_id": "ABC123",
          "status": "available",
          "product_name": "ワイヤレスイヤホン",
          "price": 2000,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "AUDIO",
          "categories": [
            "アウトドア",
            "防水"
          ]
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-products/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "prefix": {
      "product_name.keyword": "ワイヤレス"
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
    "max_score": 1.0,
    "hits": [
      {
        "_index": "lbv-7e280f3b-products",
        "_id": "ABC123",
        "_score": 1.0,
        "_source": {
          "product_id": "ABC123",
          "status": "available",
          "product_name": "ワイヤレスイヤホン",
          "price": 2000,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "AUDIO",
          "categories": [
            "アウトドア",
            "防水"
          ]
        }
      },
      {
        "_index": "lbv-7e280f3b-products",
        "_id": "C",
        "_score": 1.0,
        "_source": {
          "product_id": "C",
          "status": "available",
          "product_name": "ワイヤレススピーカー",
          "price": 500,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "ELEC",
          "categories": [
            "アウトドア"
          ]
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-products/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "match": {
      "product_name": "ワイヤレスイヤホン"
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
    "max_score": 0.394961,
    "hits": [
      {
        "_index": "lbv-7e280f3b-products",
        "_id": "ABC123",
        "_score": 0.394961,
        "_source": {
          "product_id": "ABC123",
          "status": "available",
          "product_name": "ワイヤレスイヤホン",
          "price": 2000,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "AUDIO",
          "categories": [
            "アウトドア",
            "防水"
          ]
        }
      },
      {
        "_index": "lbv-7e280f3b-products",
        "_id": "B",
        "_score": 0.25543672,
        "_source": {
          "product_id": "B",
          "status": "available",
          "product_name": "イヤホン",
          "price": 6000,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "AUDIO",
          "categories": [
            "アウトドア"
          ]
        }
      },
      {
        "_index": "lbv-7e280f3b-products",
        "_id": "C",
        "_score": 0.1974805,
        "_source": {
          "product_id": "C",
          "status": "available",
          "product_name": "ワイヤレススピーカー",
          "price": 500,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "ELEC",
          "categories": [
            "アウトドア"
          ]
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-products/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "range": {
      "price": {
        "gte": 1000,
        "lte": 5000
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
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "lbv-7e280f3b-products",
        "_id": "ABC123",
        "_score": 1.0,
        "_source": {
          "product_id": "ABC123",
          "status": "available",
          "product_name": "ワイヤレスイヤホン",
          "price": 2000,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "AUDIO",
          "categories": [
            "アウトドア",
            "防水"
          ]
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-products/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "range": {
      "created_at": {
        "gte": "2024-12-01",
        "lte": "2025-01-15"
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
        "_index": "lbv-7e280f3b-products",
        "_id": "ABC123",
        "_score": 1.0,
        "_source": {
          "product_id": "ABC123",
          "status": "available",
          "product_name": "ワイヤレスイヤホン",
          "price": 2000,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "AUDIO",
          "categories": [
            "アウトドア",
            "防水"
          ]
        }
      },
      {
        "_index": "lbv-7e280f3b-products",
        "_id": "B",
        "_score": 1.0,
        "_source": {
          "product_id": "B",
          "status": "available",
          "product_name": "イヤホン",
          "price": 6000,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "AUDIO",
          "categories": [
            "アウトドア"
          ]
        }
      },
      {
        "_index": "lbv-7e280f3b-products",
        "_id": "C",
        "_score": 1.0,
        "_source": {
          "product_id": "C",
          "status": "available",
          "product_name": "ワイヤレススピーカー",
          "price": 500,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "ELEC",
          "categories": [
            "アウトドア"
          ]
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-products/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "range": {
      "created_at": {
        "gte": "01/12/2024",
        "lte": "15/01/2025",
        "format": "dd/MM/yyyy"
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
        "_index": "lbv-7e280f3b-products",
        "_id": "ABC123",
        "_score": 1.0,
        "_source": {
          "product_id": "ABC123",
          "status": "available",
          "product_name": "ワイヤレスイヤホン",
          "price": 2000,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "AUDIO",
          "categories": [
            "アウトドア",
            "防水"
          ]
        }
      },
      {
        "_index": "lbv-7e280f3b-products",
        "_id": "B",
        "_score": 1.0,
        "_source": {
          "product_id": "B",
          "status": "available",
          "product_name": "イヤホン",
          "price": 6000,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "AUDIO",
          "categories": [
            "アウトドア"
          ]
        }
      },
      {
        "_index": "lbv-7e280f3b-products",
        "_id": "C",
        "_score": 1.0,
        "_source": {
          "product_id": "C",
          "status": "available",
          "product_name": "ワイヤレススピーカー",
          "price": 500,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "ELEC",
          "categories": [
            "アウトドア"
          ]
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-products/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "terms": {
      "category_code": [
        "ELEC",
        "AUDIO",
        "WEAR"
      ]
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
        "_index": "lbv-7e280f3b-products",
        "_id": "ABC123",
        "_score": 1.0,
        "_source": {
          "product_id": "ABC123",
          "status": "available",
          "product_name": "ワイヤレスイヤホン",
          "price": 2000,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "AUDIO",
          "categories": [
            "アウトドア",
            "防水"
          ]
        }
      },
      {
        "_index": "lbv-7e280f3b-products",
        "_id": "B",
        "_score": 1.0,
        "_source": {
          "product_id": "B",
          "status": "available",
          "product_name": "イヤホン",
          "price": 6000,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "AUDIO",
          "categories": [
            "アウトドア"
          ]
        }
      },
      {
        "_index": "lbv-7e280f3b-products",
        "_id": "C",
        "_score": 1.0,
        "_source": {
          "product_id": "C",
          "status": "available",
          "product_name": "ワイヤレススピーカー",
          "price": 500,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "ELEC",
          "categories": [
            "アウトドア"
          ]
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-products/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "product_name": "ワイヤレス"
          }
        },
        {
          "match": {
            "product_name": "イヤホン"
          }
        }
      ]
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
    "max_score": 0.394961,
    "hits": [
      {
        "_index": "lbv-7e280f3b-products",
        "_id": "ABC123",
        "_score": 0.394961,
        "_source": {
          "product_id": "ABC123",
          "status": "available",
          "product_name": "ワイヤレスイヤホン",
          "price": 2000,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "AUDIO",
          "categories": [
            "アウトドア",
            "防水"
          ]
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-products/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "bool": {
      "must": [
        {
          "terms": {
            "categories": [
              "アウトドア"
            ]
          }
        },
        {
          "terms": {
            "categories": [
              "防水"
            ]
          }
        }
      ]
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
    "max_score": 2.0,
    "hits": [
      {
        "_index": "lbv-7e280f3b-products",
        "_id": "ABC123",
        "_score": 2.0,
        "_source": {
          "product_id": "ABC123",
          "status": "available",
          "product_name": "ワイヤレスイヤホン",
          "price": 2000,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "AUDIO",
          "categories": [
            "アウトドア",
            "防水"
          ]
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-products/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "term": {
      "product_id": "ABC123"
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
    "max_score": 1.0,
    "hits": [
      {
        "_index": "lbv-7e280f3b-products",
        "_id": "ABC123",
        "_score": 1.0,
        "_source": {
          "product_id": "ABC123",
          "status": "available",
          "product_name": "ワイヤレスイヤホン",
          "price": 2000,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "AUDIO",
          "categories": [
            "アウトドア",
            "防水"
          ]
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-products/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "prefix": {
      "product_name.keyword": "ワイヤレス"
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
    "max_score": 1.0,
    "hits": [
      {
        "_index": "lbv-7e280f3b-products",
        "_id": "ABC123",
        "_score": 1.0,
        "_source": {
          "product_id": "ABC123",
          "status": "available",
          "product_name": "ワイヤレスイヤホン",
          "price": 2000,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "AUDIO",
          "categories": [
            "アウトドア",
            "防水"
          ]
        }
      },
      {
        "_index": "lbv-7e280f3b-products",
        "_id": "C",
        "_score": 1.0,
        "_source": {
          "product_id": "C",
          "status": "available",
          "product_name": "ワイヤレススピーカー",
          "price": 500,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "ELEC",
          "categories": [
            "アウトドア"
          ]
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-products/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "match": {
      "product_name": "ワイヤレスイヤホン"
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
    "max_score": 0.394961,
    "hits": [
      {
        "_index": "lbv-7e280f3b-products",
        "_id": "ABC123",
        "_score": 0.394961,
        "_source": {
          "product_id": "ABC123",
          "status": "available",
          "product_name": "ワイヤレスイヤホン",
          "price": 2000,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "AUDIO",
          "categories": [
            "アウトドア",
            "防水"
          ]
        }
      },
      {
        "_index": "lbv-7e280f3b-products",
        "_id": "B",
        "_score": 0.25543672,
        "_source": {
          "product_id": "B",
          "status": "available",
          "product_name": "イヤホン",
          "price": 6000,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "AUDIO",
          "categories": [
            "アウトドア"
          ]
        }
      },
      {
        "_index": "lbv-7e280f3b-products",
        "_id": "C",
        "_score": 0.1974805,
        "_source": {
          "product_id": "C",
          "status": "available",
          "product_name": "ワイヤレススピーカー",
          "price": 500,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "ELEC",
          "categories": [
            "アウトドア"
          ]
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-products/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "match_phrase": {
      "product_name": "ワイヤレスイヤホン"
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
    "max_score": 0.394961,
    "hits": [
      {
        "_index": "lbv-7e280f3b-products",
        "_id": "ABC123",
        "_score": 0.394961,
        "_source": {
          "product_id": "ABC123",
          "status": "available",
          "product_name": "ワイヤレスイヤホン",
          "price": 2000,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "AUDIO",
          "categories": [
            "アウトドア",
            "防水"
          ]
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-products/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "match": {
      "product_name": {
        "query": "ワイヤレス イヤホン",
        "operator": "and"
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
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.394961,
    "hits": [
      {
        "_index": "lbv-7e280f3b-products",
        "_id": "ABC123",
        "_score": 0.394961,
        "_source": {
          "product_id": "ABC123",
          "status": "available",
          "product_name": "ワイヤレスイヤホン",
          "price": 2000,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "AUDIO",
          "categories": [
            "アウトドア",
            "防水"
          ]
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-products/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "range": {
      "price": {
        "gte": 1000,
        "lte": 5000
      }
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
        "_index": "lbv-7e280f3b-products",
        "_id": "ABC123",
        "_score": 1.0,
        "_source": {
          "product_id": "ABC123",
          "status": "available",
          "product_name": "ワイヤレスイヤホン",
          "price": 2000,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "AUDIO",
          "categories": [
            "アウトドア",
            "防水"
          ]
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-products/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "terms": {
      "category_code": [
        "ELEC",
        "AUDIO",
        "WEAR"
      ]
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
        "_index": "lbv-7e280f3b-products",
        "_id": "ABC123",
        "_score": 1.0,
        "_source": {
          "product_id": "ABC123",
          "status": "available",
          "product_name": "ワイヤレスイヤホン",
          "price": 2000,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "AUDIO",
          "categories": [
            "アウトドア",
            "防水"
          ]
        }
      },
      {
        "_index": "lbv-7e280f3b-products",
        "_id": "B",
        "_score": 1.0,
        "_source": {
          "product_id": "B",
          "status": "available",
          "product_name": "イヤホン",
          "price": 6000,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "AUDIO",
          "categories": [
            "アウトドア"
          ]
        }
      },
      {
        "_index": "lbv-7e280f3b-products",
        "_id": "C",
        "_score": 1.0,
        "_source": {
          "product_id": "C",
          "status": "available",
          "product_name": "ワイヤレススピーカー",
          "price": 500,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "ELEC",
          "categories": [
            "アウトドア"
          ]
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-products/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "match_all": {}
  },
  "sort": [
    {
      "price": "asc"
    },
    {
      "release_date": "desc"
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
        "_index": "lbv-7e280f3b-products",
        "_id": "C",
        "_score": null,
        "_source": {
          "product_id": "C",
          "status": "available",
          "product_name": "ワイヤレススピーカー",
          "price": 500,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "ELEC",
          "categories": [
            "アウトドア"
          ]
        },
        "sort": [
          500,
          1734220800000
        ]
      },
      {
        "_index": "lbv-7e280f3b-products",
        "_id": "ABC123",
        "_score": null,
        "_source": {
          "product_id": "ABC123",
          "status": "available",
          "product_name": "ワイヤレスイヤホン",
          "price": 2000,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "AUDIO",
          "categories": [
            "アウトドア",
            "防水"
          ]
        },
        "sort": [
          2000,
          1734220800000
        ]
      },
      {
        "_index": "lbv-7e280f3b-products",
        "_id": "B",
        "_score": null,
        "_source": {
          "product_id": "B",
          "status": "available",
          "product_name": "イヤホン",
          "price": 6000,
          "created_at": "2024-12-15",
          "release_date": "2024-12-15",
          "category_code": "AUDIO",
          "categories": [
            "アウトドア"
          ]
        },
        "sort": [
          6000,
          1734220800000
        ]
      }
    ]
  }
}
```

判定時の補足:

```json
[
  {
    "query": {
      "term": {
        "product_id": "ABC123"
      }
    },
    "ids": [
      "ABC123"
    ]
  },
  {
    "query": {
      "prefix": {
        "product_name.keyword": "ワイヤレス"
      }
    },
    "ids": [
      "ABC123",
      "C"
    ]
  },
  {
    "query": {
      "match": {
        "product_name": "ワイヤレスイヤホン"
      }
    },
    "ids": [
      "ABC123",
      "B",
      "C"
    ]
  },
  {
    "query": {
      "range": {
        "price": {
          "gte": 1000,
          "lte": 5000
        }
      }
    },
    "ids": [
      "ABC123"
    ]
  },
  {
    "query": {
      "range": {
        "created_at": {
          "gte": "2024-12-01",
          "lte": "2025-01-15"
        }
      }
    },
    "ids": [
      "ABC123",
      "B",
      "C"
    ]
  },
  {
    "query": {
      "range": {
        "created_at": {
          "gte": "01/12/2024",
          "lte": "15/01/2025",
          "format": "dd/MM/yyyy"
        }
      }
    },
    "ids": [
      "ABC123",
      "B",
      "C"
    ]
  },
  {
    "query": {
      "terms": {
        "category_code": [
          "ELEC",
          "AUDIO",
          "WEAR"
        ]
      }
    },
    "ids": [
      "ABC123",
      "B",
      "C"
    ]
  },
  {
    "query": {
      "bool": {
        "must": [
          {
            "match": {
              "product_name": "ワイヤレス"
            }
          },
          {
            "match": {
              "product_name": "イヤホン"
            }
          }
        ]
      }
    },
    "ids": [
      "ABC123"
    ]
  },
  {
    "query": {
      "bool": {
        "must": [
          {
            "terms": {
              "categories": [
                "アウトドア"
              ]
            }
          },
          {
            "terms": {
              "categories": [
                "防水"
              ]
            }
          }
        ]
      }
    },
    "ids": [
      "ABC123"
    ]
  }
]
```
