# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch10_60_alias_switch: PASS

第10章 10.3 — replica setting and write alias switching

### PUT /lbv-7e280f3b-alias-a

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "v": {
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
  "index": "lbv-7e280f3b-alias-a"
}
```

### PUT /lbv-7e280f3b-alias-b

リクエスト:

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "v": {
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
  "index": "lbv-7e280f3b-alias-b"
}
```

### POST /_aliases

リクエスト:

```json
{
  "actions": [
    {
      "add": {
        "index": "lbv-7e280f3b-alias-a",
        "alias": "lbv-7e280f3b-write",
        "is_write_index": true
      }
    }
  ]
}
```

応答: HTTP 200

```json
{
  "acknowledged": true
}
```

### PUT /lbv-7e280f3b-write/_doc/a?refresh=true

リクエスト:

```json
{
  "v": "a"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-alias-a",
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

### POST /_aliases

リクエスト:

```json
{
  "actions": [
    {
      "remove": {
        "index": "lbv-7e280f3b-alias-a",
        "alias": "lbv-7e280f3b-write"
      }
    },
    {
      "add": {
        "index": "lbv-7e280f3b-alias-b",
        "alias": "lbv-7e280f3b-write",
        "is_write_index": true
      }
    }
  ]
}
```

応答: HTTP 200

```json
{
  "acknowledged": true
}
```

### PUT /lbv-7e280f3b-write/_doc/b?refresh=true

リクエスト:

```json
{
  "v": "b"
}
```

応答: HTTP 201

```json
{
  "_index": "lbv-7e280f3b-alias-b",
  "_id": "b",
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

### POST /lbv-7e280f3b-alias-a/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "match_all": {}
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
        "_index": "lbv-7e280f3b-alias-a",
        "_id": "a",
        "_score": 1.0,
        "_source": {
          "v": "a"
        }
      }
    ]
  }
}
```

### POST /lbv-7e280f3b-alias-b/_search

リクエスト:

```json
{
  "size": 100,
  "query": {
    "match_all": {}
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
        "_index": "lbv-7e280f3b-alias-b",
        "_id": "b",
        "_score": 1.0,
        "_source": {
          "v": "b"
        }
      }
    ]
  }
}
```

### PUT /lbv-7e280f3b-alias-b/_settings

リクエスト:

```json
{
  "index": {
    "number_of_replicas": 1
  }
}
```

応答: HTTP 200

```json
{
  "acknowledged": true
}
```

### GET /_cluster/health/lbv-7e280f3b-alias-b

応答: HTTP 200

```json
{
  "cluster_name": "docker-cluster",
  "status": "yellow",
  "timed_out": false,
  "number_of_nodes": 1,
  "number_of_data_nodes": 1,
  "discovered_master": true,
  "discovered_cluster_manager": true,
  "active_primary_shards": 1,
  "active_shards": 1,
  "relocating_shards": 0,
  "initializing_shards": 0,
  "unassigned_shards": 1,
  "delayed_unassigned_shards": 0,
  "number_of_pending_tasks": 0,
  "number_of_in_flight_fetch": 0,
  "task_max_waiting_in_queue_millis": 0,
  "active_shards_percent_as_number": 98.81656804733728
}
```

### PUT /lbv-7e280f3b-alias-b/_settings

リクエスト:

```json
{
  "index": {
    "number_of_replicas": 0
  }
}
```

応答: HTTP 200

```json
{
  "acknowledged": true
}
```

判定時の補足:

```json
{
  "single_node_with_one_replica": "yellow",
  "alias_switch": "pass"
}
```
