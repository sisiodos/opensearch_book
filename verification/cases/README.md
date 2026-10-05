# 検証ケース一覧

各ファイルの `run()` に準備・操作・期待結果（assert）を記載しています。各ケースは `python3 verification/run.py --case <ID>` で単独実行できます。

| ケース | 章・節 | 検証内容 | 過去の記録 |
| --- | --- | --- | --- |
| [ch01_01_replace_id](ch01_01_replace_id.py) | 1章 1.1 | same _id replaces one document | [HTTP記録](../evidence/ch01_01_replace_id/review.md) |
| [ch01_02_basic_values](ch01_02_basic_values.py) | 1章 1.2–1.3 | filter then aggregation/sort and source retrieval | [HTTP記録](../evidence/ch01_02_basic_values/review.md) |
| [ch02_03_term_match](ch02_03_term_match.py) | 2章 2.1.1 / 2.1.4 | term is raw; match analyzes text | [HTTP記録](../evidence/ch02_03_term_match/review.md) |
| [ch02_04_bool_array](ch02_04_bool_array.py) | 2章 2.1.5 | boolean and keyword array containment | [HTTP記録](../evidence/ch02_04_bool_array/review.md) |
| [ch02_05_ranges](ch02_05_ranges.py) | 2章 2.2.1 / 2.2.5 | numeric and parsed date range | [HTTP記録](../evidence/ch02_05_ranges/review.md) |
| [ch02_06_date_nanos](ch02_06_date_nanos.py) | 2章 2.2.5 | date_nanos retains fractional precision | [HTTP記録](../evidence/ch02_06_date_nanos/review.md) |
| [ch02_07_dv_only](ch02_07_dv_only.py) | 2章 2.3.4 | DocValues-only range, aggregate and sort | [HTTP記録](../evidence/ch02_07_dv_only/review.md) |
| [ch02_08_skip_list](ch02_08_skip_list.py) | 2章 2.3.4 | skip_list mapping and range | [HTTP記録](../evidence/ch02_08_skip_list/review.md) |
| [ch02_09_derived](ch02_09_derived.py) | 2章 2.3.3 | derived source reconstructs keyword array | [HTTP記録](../evidence/ch02_09_derived/review.md) |
| [ch03_10_field_capabilities](ch03_10_field_capabilities.py) | 3章 3.2–3.3 | field capabilities by type | [HTTP記録](../evidence/ch03_10_field_capabilities/review.md) |
| [ch03_11_caps](ch03_11_caps.py) | 3章 3.2 | assert default field capabilities for all table types | [HTTP記録](../evidence/ch03_11_caps/review.md) |
| [ch03_12_geo_values](ch03_12_geo_values.py) | 3章 3.2 / 3.3 | geo_point sorting and aggregation | [HTTP記録](../evidence/ch03_12_geo_values/review.md) |
| [ch03_13_text_dv](ch03_13_text_dv.py) | 3章 3.2 / 3.4 | text accepts but ignores doc_values true and false | [HTTP記録](../evidence/ch03_13_text_dv/review.md) |
| [ch03_14_reject_search](ch03_14_reject_search.py) | 3章 3.4 | text aggregation fails without fielddata | [HTTP記録](../evidence/ch03_14_reject_search/review.md) |
| [ch03_15_keyword_range](ch03_15_keyword_range.py) | 3章 3.4 | keyword lexicographic range differs from numeric | [HTTP記録](../evidence/ch03_15_keyword_range/review.md) |
| [ch03_16_four_combinations](ch03_16_four_combinations.py) | 3章 3.4–3.5 | index/doc_values four combinations | [HTTP記録](../evidence/ch03_16_four_combinations/review.md) |
| [ch03_17_disabled_object](ch03_17_disabled_object.py) | 3章 3.3 / 3.5 | enabled false retains arbitrary object | [HTTP記録](../evidence/ch03_17_disabled_object/review.md) |
| [ch03_18_numeric_validation](ch03_18_numeric_validation.py) | 3章 3.5 | index false still validates numeric input | [HTTP記録](../evidence/ch03_18_numeric_validation/review.md) |
| [ch03_19_source_facets](ch03_19_source_facets.py) | 3章 3.6 | source filtering and facets in one request | [HTTP記録](../evidence/ch03_19_source_facets/review.md) |
| [ch04_20_collapse](ch04_20_collapse.py) | 4章 4.2 / 4.3 | SKU collapse changes hits but not aggregation grain | [HTTP記録](../evidence/ch04_20_collapse/review.md) |
| [ch04_21_dual_read_models](ch04_21_dual_read_models.py) | 4章 4.3 | product and SKU indexes from same source | [HTTP記録](../evidence/ch04_21_dual_read_models/review.md) |
| [ch04_22_history_grain](ch04_22_history_grain.py) | 4章 4.5 | history document count differs from people count | [HTTP記録](../evidence/ch04_22_history_grain/review.md) |
| [ch05_23_chapter5_search](ch05_23_chapter5_search.py) | 5章 5.2–5.7 | book exact/prefix/match/phrase/range/terms/AND/sort examples | [HTTP記録](../evidence/ch05_23_chapter5_search/review.md) |
| [ch05_24_rolling_dates](ch05_24_rolling_dates.py) | 5章 5.4 | rolling 30 days excludes future dates | [HTTP記録](../evidence/ch05_24_rolling_dates/review.md) |
| [ch05_25_date_format](ch05_25_date_format.py) | 5章 5.4 | query format accepts dd/MM/yyyy | [HTTP記録](../evidence/ch05_25_date_format/review.md) |
| [ch05_26_millis](ch05_26_millis.py) | 5章 5.4 | date format does not preserve nanosecond precision | [HTTP記録](../evidence/ch05_26_millis/review.md) |
| [ch05_27_exists_matrix](ch05_27_exists_matrix.py) | 5章 5.8 | exists/null/empty/ignore_above behavior | [HTTP記録](../evidence/ch05_27_exists_matrix/review.md) |
| [ch05_28_null_value](ch05_28_null_value.py) | 5章 5.8 | null_value distinguishes explicit null from missing | [HTTP記録](../evidence/ch05_28_null_value/review.md) |
| [ch05_29_function_scores](ch05_29_function_scores.py) | 5章 5.9 | log1p multiply yields zero for zero/missing count | [HTTP記録](../evidence/ch05_29_function_scores/review.md) |
| [ch05_30_script_scores](ch05_30_script_scores.py) | 5章 5.9 | script_score replaces lexical score | [HTTP記録](../evidence/ch05_30_script_scores/review.md) |
| [ch05_31_stock](ch05_31_stock.py) | 5章 5.10 | exists inventory vs quantity > 0 | [HTTP記録](../evidence/ch05_31_stock/review.md) |
| [ch05_32_filter_score](ch05_32_filter_score.py) | 5章 5.10 | filter does not add score | [HTTP記録](../evidence/ch05_32_filter_score/review.md) |
| [ch05_33_should_default](ch05_33_should_default.py) | 5章 5.10 | should optional only with must/filter by default | [HTTP記録](../evidence/ch05_33_should_default/review.md) |
| [ch06_34_object_nested](ch06_34_object_nested.py) | 6章 6.1.1 / 6.2.2 | object false positive vs nested same-element match | [HTTP記録](../evidence/ch06_34_object_nested/review.md) |
| [ch06_35_dynamic_keys](ch06_35_dynamic_keys.py) | 6章 6.1.2 | dynamic keys grow mapping; repeated values do not | [HTTP記録](../evidence/ch06_35_dynamic_keys/review.md) |
| [ch06_36_flat_object](ch06_36_flat_object.py) | 6章 6.1.3 | flat_object keeps keys out of mapping and exact lookup | [HTTP記録](../evidence/ch06_36_flat_object/review.md) |
| [ch06_37_nested_scopes](ch06_37_nested_scopes.py) | 6章 6.2.2 | separate nested queries can match different elements | [HTTP記録](../evidence/ch06_37_nested_scopes/review.md) |
| [ch06_38_scalar_pairs](ch06_38_scalar_pairs.py) | 6章 6.2.3 | application scalar pair key exact match | [HTTP記録](../evidence/ch06_38_scalar_pairs/review.md) |
| [ch06_39_nested_count](ch06_39_nested_count.py) | 6章 6.2.5 | 100 nested objects produce 101 Lucene documents | [HTTP記録](../evidence/ch06_39_nested_count/review.md) |
| [ch06_40_nestedagg](ch06_40_nestedagg.py) | 6章 6.2.5 | nested aggregation counts child scope | [HTTP記録](../evidence/ch06_40_nestedagg/review.md) |
| [ch06_41_nested_limits](ch06_41_nested_limits.py) | 6章 6.2.5 | depth/nested_fields/nested_objects limits reject excess | [HTTP記録](../evidence/ch06_41_nested_limits/review.md) |
| [ch07_42_analysis_basics](ch07_42_analysis_basics.py) | 7章 7.1–7.2 | standard analyzer vs tokenizer vs keyword | [HTTP記録](../evidence/ch07_42_analysis_basics/review.md) |
| [ch07_43_keyword_normalizer](ch07_43_keyword_normalizer.py) | 7章 7.1.3 | keyword rejects analyzer; normalizer retains one term | [HTTP記録](../evidence/ch07_43_keyword_normalizer/review.md) |
| [ch07_44_textkeyword](ch07_44_textkeyword.py) | 7章 7.1.3 | text with keyword analyzer remains text without aggregation | [HTTP記録](../evidence/ch07_44_textkeyword/review.md) |
| [ch07_45_kuromoji](ch07_45_kuromoji.py) | 7章 7.2 | kuromoji tokenizer on Japanese example | [HTTP記録](../evidence/ch07_45_kuromoji/review.md) |
| [ch07_46_custom_ja](ch07_46_custom_ja.py) | 7章 7.3.3 | complete custom_ja book mapping and search synonyms | [HTTP記録](../evidence/ch07_46_custom_ja/review.md) |
| [ch07_47_natural_search](ch07_47_natural_search.py) | 7章 7.4.3 | natural_search definition and explicit Japanese stopwords | [HTTP記録](../evidence/ch07_47_natural_search/review.md) |
| [ch07_48_faq_search](ch07_48_faq_search.py) | 7章 7.4.5 | faq_query multi-word synonym graph | [HTTP記録](../evidence/ch07_48_faq_search/review.md) |
| [ch07_49_query_types](ch07_49_query_types.py) | 7章 7.4.1 | term/match/phrase/prefix/wildcard/regexp differences | [HTTP記録](../evidence/ch07_49_query_types/review.md) |
| [ch08_50_geo_formats](ch08_50_geo_formats.py) | 8章 8.2 | three coordinate formats give same search results | [HTTP記録](../evidence/ch08_50_geo_formats/review.md) |
| [ch08_51_geo_queries](ch08_51_geo_queries.py) | 8章 8.3 | book distance, box and polygon queries on points | [HTTP記録](../evidence/ch08_51_geo_queries/review.md) |
| [ch08_52_geo_rank](ch08_52_geo_rank.py) | 8章 8.4 | distance sort and gauss decay at scale | [HTTP記録](../evidence/ch08_52_geo_rank/review.md) |
| [ch08_53_geo_shapes](ch08_53_geo_shapes.py) | 8章 8.5 | point array and geo_shape line/polygon fields | [HTTP記録](../evidence/ch08_53_geo_shapes/review.md) |
| [ch09_54_bm25_formula](ch09_54_bm25_formula.py) | 9章 9.2.2 | BM25 explain agrees with book formula | [HTTP記録](../evidence/ch09_54_bm25_formula/review.md) |
| [ch09_55_legacy_bm25](ch09_55_legacy_bm25.py) | 9章 9.2.2 | LegacyBM25 scaling versus current BM25 | [HTTP記録](../evidence/ch09_55_legacy_bm25/review.md) |
| [ch09_56_title_boost](ch09_56_title_boost.py) | 9章 9.3.2 | title boost raises title match | [HTTP記録](../evidence/ch09_56_title_boost/review.md) |
| [ch09_57_popularity](ch09_57_popularity.py) | 9章 9.3.3 | sqrt(factor * popularity) multiply formula | [HTTP記録](../evidence/ch09_57_popularity/review.md) |
| [ch09_58_custom_bm25](ch09_58_custom_bm25.py) | 9章 9.3.4 | custom BM25 k1/b settings change score | [HTTP記録](../evidence/ch09_58_custom_bm25/review.md) |
| [ch10_59_refresh_visibility](ch10_59_refresh_visibility.py) | 10章 10.1 / 10.4 | refresh visibility and segment/flush APIs | [HTTP記録](../evidence/ch10_59_refresh_visibility/review.md) |
| [ch10_60_alias_switch](ch10_60_alias_switch.py) | 10章 10.3 | replica setting and write alias switching | [HTTP記録](../evidence/ch10_60_alias_switch/review.md) |
