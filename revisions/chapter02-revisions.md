# 第2章 改訂記録

改訂日：2026-10-03

第2章では、語から文書を探す Posting List、数値や空間の範囲を絞る BKD Tree、文書から値を読む DocValues を学びます。初学者がフィールド設計の理由を理解できるよう、それぞれの得意な役割を説明し、実際の検索では構造を組み合わせて使う視点を示しています。

改訂内容を、用語・説明などの訂正（errata）と、説明の充実・整理や実装バージョンへの対応（revised）に分類しています。

## errata

| 節 | 改訂後の内容 |
| --- | --- |
| 2.1 / 2.1.2 転置インデックス | Posting List を語を含む文書の一覧として紹介し、語を探す辞書と分けて説明しています。BlockTree では語をブロックに保存し、FST を到達のための索引として使います。 |
| 2.1.5 配列の索引 | 配列の要素はフィールド型に応じた構造で扱うことを説明しています。keyword 配列の包含検索と、object 配列の属性間関係を分けています。 |
| 2.2.2 範囲検索の処理量 | 条件に合わない領域を読み飛ばす仕組みを説明し、検索範囲、一致件数、値の分布によって処理量が変わることを示しています。 |
| 2.2.5 日時の入力と型 | 文字列で入力した日時も、date として定義すれば解析して数値で扱うことを説明しています。date のミリ秒と date_nanos のナノ秒を区別しています。 |
| 2.2 脚注 | BKD Tree の実装と背景論文を参照できる、Lucene の公式Javadocを案内しています。 |
| 2.3.4 DocValues による絞り込み | 文書から値を読み、条件に合うかを確認する検索も説明しています。索引と DocValues を条件に応じて選ぶ仕組みを紹介しています。 |

## revised

| 節 | 改訂後の内容 |
| --- | --- |
| 章冒頭 / 章末 基本の役割分担 | 三つの構造を主な役割から説明し、検索・集計・取得の目的に合わせて型や設定を選ぶ次章へつなげています。 |
| 2.1 語の単位と第1章への接続 | 検索用の語にはコードなどの値全体も含まれることを説明しています。docID の基礎説明は第1章を参照し、本章では索引の仕組みに進みます。 |
| 2.1.1 / 2.1.3 語の検索 | term と match の違いを説明し、docID の一覧を辿る処理と読み飛ばしを紹介しています。一致件数が多い場合の処理も示しています。 |
| 2.1.4 text と keyword | 単語への分割と値全体の扱いを例で説明しています。辞書に入る語の単位に焦点を当て、各型の用途と既定設定は第3章へつなげています。 |
| 2.2.1 / 2.2.3 範囲検索 | 数値・日時・座標の範囲に合わせて領域を絞る考え方を示し、実際の条件で応答時間を確認する視点を説明しています。 |
| 2.3 DocValues の基本 | 価格の列から必要な文書の値を読むイメージで、列指向の保存構造を説明しています。基本の役割分担は第1章を参照します。 |
| 2.3.2 圧縮と数値型 | 差分圧縮と bit packing を説明し、保存形式上の工夫とフィールド型が定める範囲・精度を分けています。 |
| 2.3.3 用途と取得 | 型・既定設定・用途に応じた設定判断は第3章へつなげ、本章では保存構造と実行時の使われ方に焦点を当てています。 |
| 2.3.3 derived source（version update） | 通常の _source の説明は第3章を参照し、フィールド値から _source を再構成する方法を短く紹介しています。取得する配列の順序や重複などを確認する視点を示しています。 |
| 2.3.4 skip_list（version update） | OpenSearch 3.2 で導入された、DocValues の範囲検索などを助ける補助索引を短く紹介しています。Posting List の読み飛ばしとの違いも説明しています。 |

## 参考資料

- [Lucene 10.2.1：BlockTree の語辞書と索引](https://lucene.apache.org/core/10_2_1/core/org/apache/lucene/codecs/lucene90/blocktree/Lucene90BlockTreeTermsWriter.html)
- [Lucene 10.2.1：BKD Tree](https://lucene.apache.org/core/10_2_1/core/org/apache/lucene/util/bkd/package-summary.html)
- [Lucene 10.2.1：DocValues を使う検索](https://lucene.apache.org/core/10_2_1/core/org/apache/lucene/search/IndexOrDocValuesQuery.html)
- [OpenSearch：date](https://docs.opensearch.org/latest/mappings/supported-field-types/date/)
- [OpenSearch：date_nanos](https://docs.opensearch.org/latest/mappings/supported-field-types/date-nanos/)
- [OpenSearch：DocValues](https://docs.opensearch.org/latest/mappings/mapping-parameters/doc-values/)
- [OpenSearch：_source と derived source](https://docs.opensearch.org/latest/mappings/metadata-fields/source/)
- [OpenSearch：3.2 の skip_list 導入](https://opensearch.org/blog/introducing-opensearch-3-2-next-generation-search-and-anayltics-with-enchanced-ai-capabilities/)

## 今回の更新範囲

第2章の本文に改訂を適用し、その内容に合わせて改訂記録を作成しました。既存の節番号・順序と文字列・価格・日時の例を活かし、各構造の役割からフィールド設計へ進む流れを維持しています。第1章の基礎説明と第3章の型・設定の説明との重複を整理し、本章では内部構造の仕組みを中心にしています。記録には改訂後に読者が学べる内容を記載しています。公式資料との照合と文書・差分の確認を行いました。OpenSearch 実機での性能測定と出版用レンダリングは未実施です。

2026-10-03 の実機検証では、OpenSearch 3.9.0（Lucene 10.5.1）で本章に対応する動作確認7項目が成功しました。同梱Luceneでの索引構造とdocID変更も別途確認しています。対象と前提条件、証跡、未検証範囲は [実機検証記録](../verification/REPORT.md) にまとめています。性能の一般的な保証や出版用レンダリングの確認は含みません。
