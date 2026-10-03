# 章順の実機検証対象一覧

各項目は results.json / exchanges.json に対応します。本文の例に必要な mapping、データ、検索時設定を補って実行しています。エラーを期待する設定・クエリは拒否されることを成功条件にします。

| 章・節 | 検証対象 | 結果 |
| --- | --- | --- |
| 1章 1.1 | same _id replaces one document | PASS |
| 1章 1.2–1.3 | filter then aggregation/sort and source retrieval | PASS |
| 2章 2.1.1 / 2.1.4 | term is raw; match analyzes text | PASS |
| 2章 2.1.5 | boolean and keyword array containment | PASS |
| 2章 2.2.1 / 2.2.5 | numeric and parsed date range | PASS |
| 2章 2.2.5 | date_nanos retains fractional precision | PASS |
| 2章 2.3.4 | DocValues-only range, aggregate and sort | PASS |
| 2章 2.3.4 | skip_list mapping and range | PASS |
| 2章 2.3.3 | derived source reconstructs keyword array | PASS |
| 3章 3.2–3.3 | field capabilities by type | PASS |
| 3章 3.2 / 3.3 | geo_point sorting and aggregation | PASS |
| 3章 3.2 / 3.4 | text accepts but ignores doc_values true and false | PASS |
| 3章 3.4 | text aggregation fails without fielddata | PASS |
| 3章 3.4 | keyword lexicographic range differs from numeric | PASS |
| 3章 3.4–3.5 | index/doc_values four combinations | PASS |
| 3章 3.3 / 3.5 | enabled false retains arbitrary object | PASS |
| 3章 3.5 | index false still validates numeric input | PASS |
| 3章 3.6 | source filtering and facets in one request | PASS |
| 3章 3.2 | assert default field capabilities for all table types | PASS |
| 4章 4.2 / 4.3 | SKU collapse changes hits but not aggregation grain | PASS |
| 4章 4.3 | product and SKU indexes from same source | PASS |
| 4章 4.5 | history document count differs from people count | PASS |
| 5章 5.2–5.7 | book exact/prefix/match/phrase/range/terms/AND/sort examples | PASS |
| 5章 5.4 | rolling 30 days excludes future dates | PASS |
| 5章 5.4 | query format accepts dd/MM/yyyy | PASS |
| 5章 5.8 | exists/null/empty/ignore_above behavior | PASS |
| 5章 5.8 | null_value distinguishes explicit null from missing | PASS |
| 5章 5.9 | log1p multiply yields zero for zero/missing count | PASS |
| 5章 5.9 | script_score replaces lexical score | PASS |
| 5章 5.10 | exists inventory vs quantity > 0 | PASS |
| 5章 5.10 | filter does not add score | PASS |
| 5章 5.10 | should optional only with must/filter by default | PASS |
| 5章 5.4 | date format does not preserve nanosecond precision | PASS |
| 6章 6.1.1 / 6.2.2 | object false positive vs nested same-element match | PASS |
| 6章 6.1.2 | dynamic keys grow mapping; repeated values do not | PASS |
| 6章 6.1.3 | flat_object keeps keys out of mapping and exact lookup | PASS |
| 6章 6.2.2 | separate nested queries can match different elements | PASS |
| 6章 6.2.3 | application scalar pair key exact match | PASS |
| 6章 6.2.5 | 100 nested objects produce 101 Lucene documents | PASS |
| 6章 6.2.5 | depth/nested_fields/nested_objects limits reject excess | PASS |
| 6章 6.2.5 | nested aggregation counts child scope | PASS |
| 7章 7.1–7.2 | standard analyzer vs tokenizer vs keyword | PASS |
| 7章 7.1.3 | keyword rejects analyzer; normalizer retains one term | PASS |
| 7章 7.2 | kuromoji tokenizer on Japanese example | PASS |
| 7章 7.3.3 | complete custom_ja book mapping and search synonyms | PASS |
| 7章 7.4.3 | natural_search definition and explicit Japanese stopwords | PASS |
| 7章 7.4.5 | faq_query multi-word synonym graph | PASS |
| 7章 7.4.1 | term/match/phrase/prefix/wildcard/regexp differences | PASS |
| 7章 7.1.3 | text with keyword analyzer remains text without aggregation | PASS |
| 8章 8.2 | three coordinate formats give same search results | PASS |
| 8章 8.3 | book distance, box and polygon queries on points | PASS |
| 8章 8.4 | distance sort and gauss decay at scale | PASS |
| 8章 8.5 | point array and geo_shape line/polygon fields | PASS |
| 9章 9.2.2 | BM25 explain agrees with book formula | PASS |
| 9章 9.2.2 | LegacyBM25 scaling versus current BM25 | PASS |
| 9章 9.3.2 | title boost raises title match | PASS |
| 9章 9.3.3 | sqrt(factor * popularity) multiply formula | PASS |
| 9章 9.3.4 | custom BM25 k1/b settings change score | PASS |
| 10章 10.1 / 10.4 | refresh visibility and segment/flush APIs | PASS |
| 10章 10.3 | replica setting and write alias switching | PASS |
| 1–2章 | 同梱Luceneの索引構造・docIDのマージ前後の変化 | PASS |

第10章は構成案のため、操作の基本確認だけを対象にしています。性能と本番構成の残る項目は REPORT.md を参照してください。
