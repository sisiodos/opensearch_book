# 第3章 改訂記録

改訂日：2026-10-03

第3章では、各フィールドを検索・集計・ソート・表示のどこに使うかを考え、型と設定を選びます。初学者が既定設定を出発点に設計できるよう、index、doc_values、_source の役割を分け、必要な操作に合わせて構造を作る判断を説明しています。

改訂内容を、用語・説明などの訂正（errata）と、説明の充実・整理や実装バージョンへの対応（revised）に分類しています。

## errata

| 節 | 改訂後の内容 |
| --- | --- |
| 3.1 mapping と _source | OpenSearch が mapping に従って値を解析し、Lucene の構造を作ることを説明しています。通常の _source は stored fields を通じて保存し、検索用構造とは役割を分けています。 |
| 3.2 / 3.3 位置情報 | geo_point は既定で DocValues を持ち、位置による検索、地理空間集計、距離によるソートに使えることを説明しています。 |
| 3.2 / 3.3 / 3.4 text の設定 | text は doc_values パラメータに非対応であることを示し、OpenSearch 3.9.0 の実機では指定が受理されても保持されず、DocValues が作られないことを説明しています。 |
| 3.4 数値と keyword | keyword のソートや範囲検索は文字列の順序に従うことを説明しています。数値としての比較・計算と、識別子全体の一致を区別しています。 |
| 3.3 / 3.5 保存専用の値 | スカラー値の index・doc_values の設定と、object 全体の解析を止める enabled: false を分けています。文字列と JSON オブジェクトの raw_payload の例を示しています。 |
| 3.5 / 3.6 index と doc_values | 二つの設定が独立していることを説明しています。index: false でも DocValues を残せることと、ドキュメント更新の処理は残ることを示しています。 |
| 3.4 specs の属性間関係 | key と value を同じ配列要素の条件として評価する必要があることを説明しています。通常の object 配列で別要素の値が一致する例を示しています。 |

## revised

| 節 | 改訂後の内容 |
| --- | --- |
| 3.1 / 3.2 第2章・第4章との接続 | 内部構造の仕組みは第2章、検索ドキュメントの粒度は第4章へつなぎ、本章はフィールドごとの型・設定の選択を扱います。既定設定を出発点に必要な操作を確認する流れを示しています。 |
| 3.1 derived source（version update） | 通常の _source を前提とすることを明記し、無効化・保存対象の除外・Derived source による再構成を短く補足しています。再構成の詳説は第2章へつなげています。 |
| 3.3 用途別のパターン | 既存の六つのパターンを維持し、全文検索、値全体の一致、数値・日時・位置情報の用途を説明しています。不要な構造を省く場合も、必要な操作と負荷を確認します。 |
| 3.4 text の集計とサブフィールド | fielddata の既定状態と解析後の語の集計を区別し、値全体の集計には keyword を定義することを説明しています。.keyword が定義されているかを確認する視点も示しています。 |
| 3.4 nested と第6章への接続 | 同じ要素の属性間関係が必要なら nested を選ぶ方針を示しています。固定属性を専用フィールドへ組み替える例を維持し、動的な key の増加と flat_object の役割を短く補足しています。実装と規模・負荷の管理は第6章へつなげています。 |
| 3.5 索引を省く判断 | 表示・保存だけに使う値の構造を省く考え方を説明しています。設定を名称から決めず用途から判断し、要件変更では再インデックスが必要になることを示しています。 |
| 3.6 レスポンスの設計 | 検索用構造を作る判断と応答に返す判断を分けています。_source の絞り込みは転送量を減らし、保存容量や取得処理とは別に考えることを説明しています。集計する内容に合った型を選ぶ視点も示しています。 |

## 参考資料

- [OpenSearch：text](https://docs.opensearch.org/latest/mappings/supported-field-types/text/)
- [OpenSearch：geo_point](https://docs.opensearch.org/latest/mappings/supported-field-types/geo-point/)
- [OpenSearch：index と doc_values](https://docs.opensearch.org/latest/mappings/mapping-parameters/index-parameter/)
- [OpenSearch：enabled](https://docs.opensearch.org/latest/mappings/mapping-parameters/enabled/)
- [OpenSearch：range query](https://docs.opensearch.org/latest/query-dsl/term/range/)
- [OpenSearch：nested](https://docs.opensearch.org/latest/mappings/supported-field-types/nested/)
- [OpenSearch：flat_object](https://docs.opensearch.org/latest/mappings/supported-field-types/flat-object/)
- [OpenSearch：_source と derived source](https://docs.opensearch.org/latest/mappings/metadata-fields/source/)

## 今回の更新範囲

第3章の本文に改訂を適用し、その内容に合わせて改訂記録を作成しました。既存の3.1〜3.6の構成、六つの設計パターンと五つのアンチパターン、specs と raw_payload、検索応答の例を活かしています。第2章の内部構造、第4章のドキュメント粒度、第6章の属性間関係との役割分担を維持し、フィールド設定の判断に焦点を当てています。記録には改訂後に読者が学べる内容を記載しています。公式資料との照合と文書・差分の確認を行いました。性能測定と出版用レンダリングは未実施です。

2026-10-03 の実機検証では、OpenSearch 3.9.0（Lucene 10.5.1）で本章に対応する動作確認10項目が成功しました。対象と前提条件、証跡、未検証範囲は [実機検証記録](../verification/REPORT.md) にまとめています。性能の一般的な保証や出版用レンダリングの確認は含みません。
