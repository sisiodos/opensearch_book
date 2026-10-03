# 第9章 改訂記録

改訂日：2026-10-03

第9章では、語の出現頻度と希少性からスコアの考え方を学び、確率的関連性モデル、BM25、OpenSearch での調整へと進みます。初学者が「なぜその語や文書を高く評価するのか」を理解できるよう、身近な説明から式へつなぎ、検索結果を見ながら設計する視点を重視しています。

改訂内容を、用語・数式などの訂正（errata）と、説明の充実・整理や実装バージョンへの対応（revised）に分類しています。

## errata

| 節 | 改訂後の内容 |
| --- | --- |
| 9.2.3 対数オッズ比 | 関連文書によく現れる語を、関連性を示す証拠として説明しています。語が現れる確率と現れない確率を使う「オッズ」を紹介し、語ごとの重みを足し合わせる考え方につなげています。 |
| 9.2.3 条件付き確率の推定 | 語を含む文書の割合から確率を求めます。記号 $r_t$ は、その語を含む関連文書の数を表しています。 |
| 9.2.3 IDF への接続 | 関連性の判定がないときの仮定を示し、確率的な語の重みから「珍しい語ほど重く扱う」という IDF の考え方へ段階的につなげています。 |
| 9.2.3 情報量との関係 | 非関連文書では珍しく、関連文書ではよく現れる語ほど、関連性の判断に役立つことを情報量の差で説明しています。 |
| 9.3.3 計算例 | 人気度による補正を $\sqrt{1.5\times popularity}$ と示し、その値を元の検索スコアに掛け合わせる流れを説明しています。 |

## revised

| 節 | 改訂後の内容 |
| --- | --- |
| 9.1 スコアとは何か | `_score` を、検索語と文書の関連性を数値化して順位付けに使う指標として紹介しています。確率的な考え方との関係は補足で説明しています。 |
| 9.2.1 TF–IDF | 「語の出現頻度」と「語の希少さ」を組み合わせる基本的な考え方を示し、BM25 を学ぶ足場としています。 |
| 9.2.2 BM25（version update） | OpenSearch 3.x の既定式を示しています。語の出現回数が増えると寄与が飽和することと、文書長による補正を説明し、従来の `LegacyBM25` に含まれる $(k_1+1)$ 因子も紹介しています。 |
| 9.2.3 平滑化 | 観測数に小さな補正を加えることで、確率が 0 や 1 になる場合にも安定して重みを計算する考え方を説明しています。 |
| 9.3.2 boost | タイトルを重視する例から、特徴の重要度を重みで表す考え方を紹介しています。BM25F との共通の設計課題にも触れ、評価データを使う調整から Learning to Rank へつなげています。 |
| 9.3.3 function_score | 検索条件に一致した文書に、人気度や新しさなどを反映して順位を補正する仕組みを説明しています。`score_mode` と `boost_mode` の役割を分け、検索結果を見て影響を確認する視点を示しています。 |
| 9.3.4 BM25 パラメータ | `k1` を語の出現回数の反映、`b` を文書長補正の調整として説明しています。Similarity の設定として扱い、文書やクエリに合った値を評価用データで比較します。 |
| 9.4 スコアをモデルとして捉える | BM25 を「複数の特徴量から一つのスコアを作るモデル」として捉え、線形モデルとの類似を手掛かりに L2R やハイブリッド検索へ進みます。「複数の証拠をどう表現し、統合するか」という共通の問いを中心に説明しています。 |
| 9.5 スコア設計の指針 | boost、function_score、BM25 パラメータ、L2R の役割を整理し、評価用データで順位の変化を確認する設計につなげています。 |

## 参考資料

- [OpenSearch：BM25 と実装バージョンの対応](https://docs.opensearch.org/latest/search-plugins/keyword-search/)
- [Lucene 10.2.1：BM25Similarity](https://lucene.apache.org/core/10_2_1/core/org/apache/lucene/search/similarities/BM25Similarity.html)
- [OpenSearch：multi_match](https://docs.opensearch.org/latest/query-dsl/full-text/multi-match/)
- [OpenSearch：function_score](https://docs.opensearch.org/latest/query-dsl/compound/function-score/)
- [Introduction to Information Retrieval：語の重みの導出](https://nlp.stanford.edu/IR-book/html/htmledition/deriving-a-ranking-function-for-query-terms-1.html)
- [Introduction to Information Retrieval：確率の推定](https://nlp.stanford.edu/IR-book/html/htmledition/probability-estimates-in-practice-1.html)

## 今回の更新範囲

著者が変更した第9章の現行本文に合わせて、改訂記録を更新しました。本文の説明の流れを尊重し、記録には改訂後に読者が学べる内容を記載しています。

2026-10-03 の実機検証では、OpenSearch 3.9.0（Lucene 10.5.1）で本章に対応する動作確認5項目が成功しました。対象と前提条件、証跡、未検証範囲は [実機検証記録](../verification/REPORT.md) にまとめています。性能の一般的な保証や出版用レンダリングの確認は含みません。
