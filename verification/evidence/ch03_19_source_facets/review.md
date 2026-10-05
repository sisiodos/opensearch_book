# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch03_19_source_facets: PASS

第3章 3.6 — source filtering and facets in one request

### POST /lbv-7e280f3b-basic/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "match_all": {}
  },
  "_source": [
    "name"
  ],
  "aggs": {
    "tags": {
      "terms": {
        "field": "tags"
      }
    }
  }
}
```

応答: HTTP 200

```json
{
  "took": 3,
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
        "_index": "lbv-7e280f3b-basic",
        "_id": "b",
        "_score": 1.0,
        "_source": {
          "name": "Lucene reference"
        }
      },
      {
        "_index": "lbv-7e280f3b-basic",
        "_id": "a",
        "_score": 1.0,
        "_source": {
          "name": "OpenSearch Lucene"
        }
      }
    ]
  },
  "aggregations": {
    "tags": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "blue",
          "doc_count": 1
        },
        {
          "key": "green",
          "doc_count": 1
        },
        {
          "key": "red",
          "doc_count": 1
        }
      ]
    }
  }
}
```

判定時の補足:

```json
null
```
