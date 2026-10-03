# 第7章 改訂記録

改訂日：2026-10-03

第7章では、文字列をどの単位で検索し、どの表記を同一視するかを設計します。text と keyword、tokenizer と analyzer、登録時と検索時の解析を分け、設定例から検索の理由を追えるように説明しています。

改訂内容を、用語・説明などの訂正（errata）と、説明の充実・整理や実装バージョンへの対応（revised）に分類しています。

## errata

| 節 | 改訂後の内容 |
| --- | --- |
| 7.1.1 / 7.1.3 text と keyword | keyword は analyzer を指定せず、必要に応じて normalizer を使うことを説明しています。text と keyword は語の分割だけでなく、DocValues やスコアリング情報の既定設定も異なることを示しています。 |
| 7.1.1 前方一致 | 接頭辞に一致する語を辞書から探す処理を説明し、処理量は一致する語・文書にも依存することを示しています。辞書の仕組みは第2章を参照します。 |
| 7.2 tokenizer と小文字化 | standard tokenizer の分割結果は元の大文字・小文字を維持する例とし、小文字化は後段のフィルターが担うことを説明しています。 |
| 7.2 登録時と検索時 | analyzer は同一でなくてもよく、search_analyzer によって検索時の処理を分けられることを説明しています。重要なのは両者が対応するトークンを生成することです。 |
| 7.3 analyzer の構成 | 任意の CharFilter、Tokenizer、TokenFilter の順序でトークン列を作り、登録時と検索時の双方で使う処理として説明しています。 |
| 7.3.3 / 7.4.3 / 7.4.5 設定例 | 使用する同義語フィルターを定義し、検索時に synonym_graph を使う例を示しています。最初の例には settings と mapping を含め、後続の例は検索用 analyzer の設定と適用方法を説明しています。 |
| 7.4.3 日本語の除外語 | 既定の stop は英語の除外語を使うことを説明し、日本語の除外語を明示した ja_stop を定義しています。 |

## revised

| 節 | 改訂後の内容 |
| --- | --- |
| 章冒頭 / 7.1 第6章・第3章との接続 | 第6章の属性間関係の設計から文字列の設計へつなげ、DocValues などの設定判断は第3章を参照する構成にしています。 |
| 7.1 / 7.4 語の一致と完全一致 | text の語による一致を任意の中間一致と区別しています。term での keyword 全体の一致と、normalizer を設定した場合の正規化を説明しています。 |
| 7.2 解析結果の確認 | _analyze API でトークンと語の位置を確認する方法を案内しています。 |
| 7.3.2 同義語の適用 | 展開方向、適用時点、前段のフィルターの影響を示し、複数語の同義語には検索時の synonym_graph を紹介しています。登録時の展開を変更する場合の再インデックスにも触れています。 |
| 7.4.2 再現率と適合率 | 一律の増減を示す表を、各処理の効果と注意点の表へ改めています。必要な語の除去や同一視の広げすぎを、代表的な検索例で確認する視点を示しています。 |
| 7.4.5 FAQ の例 | 辞書による同義語展開と意図の理解を区別しています。英語の略称を使う例であることを明記し、日本語では適した tokenizer を選ぶ説明を加えています。 |

## 参考資料

- [OpenSearch：normalizer](https://docs.opensearch.org/latest/analyzers/normalizers/)
- [OpenSearch：standard tokenizer](https://docs.opensearch.org/latest/analyzers/tokenizers/standard/)
- [OpenSearch：custom analyzer](https://docs.opensearch.org/latest/analyzers/custom-analyzer/)
- [OpenSearch：search_analyzer](https://docs.opensearch.org/latest/mappings/mapping-parameters/search-analyzer/)
- [OpenSearch：synonym_graph](https://docs.opensearch.org/latest/analyzers/token-filters/synonym-graph/)
- [OpenSearch：stop filter](https://docs.opensearch.org/latest/analyzers/token-filters/stop/)

## 今回の更新範囲

第7章の本文に改訂を適用し、その内容に合わせて改訂記録を作成しました。既存の7.1〜7.4と各小節の構成、OpenSearch Lucene、商品コード、日本語の自然文、FAQ の例を活かしています。検索用の語を作る設計に焦点を当て、ベクトル検索の詳説は追加していません。公式資料との照合、JSON 設定例と節構成・差分の確認を行いました。出版用レンダリングは未実施です。

2026-10-03 の実機検証では、OpenSearch 3.9.0（Lucene 10.5.1）で本章に対応する動作確認8項目が成功しました。対象と前提条件、証跡、未検証範囲は [実機検証記録](../verification/REPORT.md) にまとめています。性能の一般的な保証や出版用レンダリングの確認は含みません。
