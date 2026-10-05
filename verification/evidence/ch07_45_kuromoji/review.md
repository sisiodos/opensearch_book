# 検証の実行記録

各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。

## ch07_45_kuromoji: PASS

第7章 7.2 — kuromoji tokenizer on Japanese example

### POST /_analyze

リクエスト:

```json
{
  "tokenizer": "kuromoji_tokenizer",
  "text": "私は学生です"
}
```

応答: HTTP 200

```json
{
  "tokens": [
    {
      "token": "私",
      "start_offset": 0,
      "end_offset": 1,
      "type": "word",
      "position": 0
    },
    {
      "token": "は",
      "start_offset": 1,
      "end_offset": 2,
      "type": "word",
      "position": 1
    },
    {
      "token": "学生",
      "start_offset": 2,
      "end_offset": 4,
      "type": "word",
      "position": 2
    },
    {
      "token": "です",
      "start_offset": 4,
      "end_offset": 6,
      "type": "word",
      "position": 3
    }
  ]
}
```

判定時の補足:

```json
[
  {
    "token": "私",
    "start_offset": 0,
    "end_offset": 1,
    "type": "word",
    "position": 0
  },
  {
    "token": "は",
    "start_offset": 1,
    "end_offset": 2,
    "type": "word",
    "position": 1
  },
  {
    "token": "学生",
    "start_offset": 2,
    "end_offset": 4,
    "type": "word",
    "position": 2
  },
  {
    "token": "です",
    "start_offset": 4,
    "end_offset": 6,
    "type": "word",
    "position": 3
  }
]
```
