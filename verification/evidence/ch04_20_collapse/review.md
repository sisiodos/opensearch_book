# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch04_20_collapse: PASS

第4章 4.2 / 4.3 — SKU collapse changes hits but not aggregation grain

### PUT /lbv-7e280f3b-collapse

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "product": {
        "type": "keyword"
      },
      "sku": {
        "type": "keyword"
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
  "index": "lbv-7e280f3b-collapse"
}
```

### PUT /lbv-7e280f3b-collapse/_doc/s1?refresh=true

リクエスト:

```json
{
  "sku": "s1",
  "product": "p1"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-collapse",
  "_id": "s1",
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

### PUT /lbv-7e280f3b-collapse/_doc/s2?refresh=true

リクエスト:

```json
{
  "sku": "s2",
  "product": "p1"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-collapse",
  "_id": "s2",
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

### PUT /lbv-7e280f3b-collapse/_doc/s3?refresh=true

リクエスト:

```json
{
  "sku": "s3",
  "product": "p2"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-collapse",
  "_id": "s3",
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

### POST /lbv-7e280f3b-collapse/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "match_all": {}
  },
  "collapse": {
    "field": "product"
  },
  "aggs": {
    "products": {
      "terms": {
        "field": "product"
      }
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
      "value": 3,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "lbv-7e280f3b-collapse",
        "_id": "s1",
        "_score": 1.0,
        "_source": {
          "sku": "s1",
          "product": "p1"
        },
        "fields": {
          "product": [
            "p1"
          ]
        }
      },
      {
        "_index": "lbv-7e280f3b-collapse",
        "_id": "s3",
        "_score": 1.0,
        "_source": {
          "sku": "s3",
          "product": "p2"
        },
        "fields": {
          "product": [
            "p2"
          ]
        }
      }
    ]
  },
  "aggregations": {
    "products": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "p1",
          "doc_count": 2
        },
        {
          "key": "p2",
          "doc_count": 1
        }
      ]
    }
  }
}
```

判定時の補足:

```json
{
  "collapsed_hits": 2,
  "total": 3,
  "aggregation_docs": 3
}
```
