# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch03_10_field_capabilities: PASS

第3章 3.2–3.3 — field capabilities by type

### GET /lbv-7e280f3b-basic/_field_caps?fields=*

応答: HTTP 200

```json
{
  "indices": [
    "lbv-7e280f3b-basic"
  ],
  "fields": {
    "date": {
      "date": {
        "type": "date",
        "searchable": true,
        "aggregatable": true
      }
    },
    "_routing": {
      "_routing": {
        "type": "_routing",
        "searchable": true,
        "aggregatable": false
      }
    },
    "_doc_count": {
      "long": {
        "type": "long",
        "searchable": false,
        "aggregatable": false
      }
    },
    "code": {
      "keyword": {
        "type": "keyword",
        "searchable": true,
        "aggregatable": true
      }
    },
    "flag": {
      "boolean": {
        "type": "boolean",
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
    "display": {
      "keyword": {
        "type": "keyword",
        "searchable": false,
        "aggregatable": false
      }
    },
    "tags": {
      "keyword": {
        "type": "keyword",
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
    "price": {
      "integer": {
        "type": "integer",
        "searchable": true,
        "aggregatable": true
      }
    },
    "name": {
      "text": {
        "type": "text",
        "searchable": true,
        "aggregatable": false
      }
    },
    "location": {
      "geo_point": {
        "type": "geo_point",
        "searchable": true,
        "aggregatable": true
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
  "indices": [
    "lbv-7e280f3b-basic"
  ],
  "fields": {
    "date": {
      "date": {
        "type": "date",
        "searchable": true,
        "aggregatable": true
      }
    },
    "_routing": {
      "_routing": {
        "type": "_routing",
        "searchable": true,
        "aggregatable": false
      }
    },
    "_doc_count": {
      "long": {
        "type": "long",
        "searchable": false,
        "aggregatable": false
      }
    },
    "code": {
      "keyword": {
        "type": "keyword",
        "searchable": true,
        "aggregatable": true
      }
    },
    "flag": {
      "boolean": {
        "type": "boolean",
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
    "display": {
      "keyword": {
        "type": "keyword",
        "searchable": false,
        "aggregatable": false
      }
    },
    "tags": {
      "keyword": {
        "type": "keyword",
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
    "price": {
      "integer": {
        "type": "integer",
        "searchable": true,
        "aggregatable": true
      }
    },
    "name": {
      "text": {
        "type": "text",
        "searchable": true,
        "aggregatable": false
      }
    },
    "location": {
      "geo_point": {
        "type": "geo_point",
        "searchable": true,
        "aggregatable": true
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
