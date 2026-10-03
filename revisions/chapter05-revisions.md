# 第5章 改訂記録

改訂日：2026-10-03

第5章では、商品検索の例を通じて、検索条件に合うフィールド型とクエリを選びます。完全一致、前方一致、語による検索、範囲条件、存在確認、スコア調整を分け、読者が検索条件の意味と実際の動作を追えるように説明しています。

改訂内容を、用語・説明などの訂正（errata）と、説明の充実・整理や実装バージョンへの対応（revised）に分類しています。

## errata

| 節 | 改訂後の内容 |
| --- | --- |
| 5.3 / 5.9 match とスコア | 解析後の語の一致と、出現頻度・希少性・フィールド長などによる関連度を説明しています。語順の条件や任意の文字列の中間一致と区別しています。 |
| 5.3 前方一致と辞書 | 接頭辞に一致する語を辞書から探す処理として説明し、一致する語や文書が多い場合の処理量も示しています。辞書の仕組みは第2章へつなげています。 |
| 5.4 日付の形式と精度 | format は解析形式、date と date_nanos は保存精度を定めることを説明しています。過去30日の例に現在時刻の上限を加え、日単位の丸めと区別しています。 |
| 5.8 exists と null | 検索用の値の存在確認と、元の JSON の null・未設定を区別しています。空配列、索引から除外された値、DocValues、null_value の影響を説明しています。 |
| 5.9 スコア調整の例 | リクエストの JSON 内のコメントを本文へ移し、boost_mode は元のスコアと関数の計算結果を組み合わせる設定として説明しています。 |
| 5.10 在庫の判定 | exists は在庫情報の存在確認、range の gt: 0 は販売可能な在庫数の条件として区別しています。整数の在庫数と SKU 単位の関係にも触れています。 |
| 章末 RDB との比較 | RDB にも全文検索のランキング機能があることを踏まえ、条件による絞り込みと関連度による順位づけの使い分けを説明しています。 |

## revised

| 節 | 改訂後の内容 |
| --- | --- |
| 章冒頭 第4章との接続 | 検索目的に合わせて1件の read model をまとめる第4章から、その中のフィールド設計へつなげています。 |
| 5.1 / 5.2 型と完全一致 | numeric は数値型の総称として紹介し、文字列の完全一致には keyword、数値や日時などにはそれぞれの型を選ぶことを示しています。normalizer による表記の統一も短く紹介しています。 |
| 5.3 multi-field と日本語 | 同じ値を全文検索と完全一致・集計・ソートで使い分ける設計として説明しています。掲載 mapping は既定の analyzer を使うことを明記し、日本語の分割例は設定と確認が必要であることを示しています。 |
| 5.4 / 5.5 型と性能の判断 | 文字列としての範囲検索と日時としての比較を分け、terms と keyword の組み合わせを複数候補の一致条件として説明しています。性能を一律に保証する表現を整理しています。 |
| 5.6 AND 条件 | 複数クエリの bool + must を維持し、単一の match に operator: and を指定する方法も紹介しています。 |
| 5.9 スコア式の意味 | レビュー件数が0・欠損の場合の乗算結果、script_score が元の関連度を使わない例、入力値と欠損の前提を説明しています。 |
| 5.10 filter と should | キャッシュの効果は条件などに依存することを示し、should の一致が任意になる前提と minimum_should_match を短く補足しています。 |
| 章末 UI と検索条件 | 複数選択の AND・OR は画面の見た目から決めず、検索要件として定めることを説明しています。 |

## 参考資料

- [OpenSearch：match](https://docs.opensearch.org/latest/query-dsl/full-text/match/)
- [OpenSearch：prefix](https://docs.opensearch.org/latest/query-dsl/term/prefix/)
- [OpenSearch：date](https://docs.opensearch.org/latest/mappings/supported-field-types/date/)
- [OpenSearch：range と日付の丸め](https://docs.opensearch.org/latest/query-dsl/term/range/)
- [OpenSearch：exists](https://docs.opensearch.org/latest/query-dsl/term/exists/)
- [OpenSearch：bool](https://docs.opensearch.org/latest/query-dsl/compound/bool/)
- [OpenSearch：function_score](https://docs.opensearch.org/latest/query-dsl/compound/function-score/)
- [PostgreSQL：全文検索とランキング](https://www.postgresql.org/docs/current/textsearch-controls.html)

## 今回の更新範囲

第5章の本文に改訂を適用し、その内容に合わせて改訂記録を作成しました。既存の5.1〜5.10と章末の構成、商品 ID・商品名・価格・日時・カテゴリ・レビュー・在庫の例を維持しています。第2章の辞書構造、第3章のフィールド設定、第4章の read model、第6章の属性間関係との説明を揃えています。記録には改訂後に読者が学べる内容を記載しています。公式資料との照合と文書・差分の確認を行いました。性能測定と出版用レンダリングは未実施です。

2026-10-03 の実機検証では、OpenSearch 3.9.0（Lucene 10.5.1）で本章に対応する動作確認11項目が成功しました。対象と前提条件、証跡、未検証範囲は [実機検証記録](../verification/REPORT.md) にまとめています。性能の一般的な保証や出版用レンダリングの確認は含みません。
