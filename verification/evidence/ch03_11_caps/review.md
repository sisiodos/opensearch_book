# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch03_11_caps: PASS

第3章 3.2 — assert default field capabilities for all table types

### PUT /lbv-7e280f3b-defaults

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "t": {
        "type": "text"
      },
      "k": {
        "type": "keyword"
      },
      "n": {
        "type": "long"
      },
      "b": {
        "type": "boolean"
      },
      "d": {
        "type": "date"
      },
      "g": {
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
  "index": "lbv-7e280f3b-defaults"
}
```

### GET /lbv-7e280f3b-defaults/_field_caps?fields=*

応答: HTTP 200

```json
{
  "indices": [
    "lbv-7e280f3b-defaults"
  ],
  "fields": {
    "_routing": {
      "_routing": {
        "type": "_routing",
        "searchable": true,
        "aggregatable": false
      }
    },
    "b": {
      "boolean": {
        "type": "boolean",
        "searchable": true,
        "aggregatable": true
      }
    },
    "_doc_count": {
      "long": {
        "type": "long",
        "searchable": false,
        "aggregatable": false
      }
    },
    "d": {
      "date": {
        "type": "date",
        "searchable": true,
        "aggregatable": true
      }
    },
    "_index": {
      "_index": {
        "type": "_index",
        "searchable": true,
        "aggregatable": true
      }
    },
    "_feature": {
      "_feature": {
        "type": "_feature",
        "searchable": false,
        "aggregatable": false
      }
    },
    "g": {
      "geo_point": {
        "type": "geo_point",
        "searchable": true,
        "aggregatable": true
      }
    },
    "k": {
      "keyword": {
        "type": "keyword",
        "searchable": true,
        "aggregatable": true
      }
    },
    "n": {
      "long": {
        "type": "long",
        "searchable": true,
        "aggregatable": true
      }
    },
    "_ignored": {
      "_ignored": {
        "type": "_ignored",
        "searchable": true,
        "aggregatable": false
      }
    },
    "_seq_no": {
      "_seq_no": {
        "type": "_seq_no",
        "searchable": true,
        "aggregatable": true
      }
    },
    "t": {
      "text": {
        "type": "text",
        "searchable": true,
        "aggregatable": false
      }
    },
    "_nested_path": {
      "_nested_path": {
        "type": "_nested_path",
        "searchable": true,
        "aggregatable": false
      }
    },
    "_field_names": {
      "_field_names": {
        "type": "_field_names",
        "searchable": true,
        "aggregatable": false
      }
    },
    "_data_stream_timestamp": {
      "_data_stream_timestamp": {
        "type": "_data_stream_timestamp",
        "searchable": false,
        "aggregatable": false
      }
    },
    "_source": {
      "_source": {
        "type": "_source",
        "searchable": false,
        "aggregatable": false
      }
    },
    "_id": {
      "_id": {
        "type": "_id",
        "searchable": true,
        "aggregatable": true
      }
    },
    "_version": {
      "_version": {
        "type": "_version",
        "searchable": false,
        "aggregatable": false
      }
    }
  }
}
```

判定時の補足:

```json
{
  "t": {
    "text": {
      "type": "text",
      "searchable": true,
      "aggregatable": false
    }
  },
  "k": {
    "keyword": {
      "type": "keyword",
      "searchable": true,
      "aggregatable": true
    }
  },
  "n": {
    "long": {
      "type": "long",
      "searchable": true,
      "aggregatable": true
    }
  },
  "b": {
    "boolean": {
      "type": "boolean",
      "searchable": true,
      "aggregatable": true
    }
  },
  "d": {
    "date": {
      "type": "date",
      "searchable": true,
      "aggregatable": true
    }
  },
  "g": {
    "geo_point": {
      "type": "geo_point",
      "searchable": true,
      "aggregatable": true
    }
  }
}
```
