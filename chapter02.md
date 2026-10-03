# 第 2 章：Lucene のストレージ構造を理解する

この章では、Lucene における 3 つの主要なストレージ構造 ──Posting List、BKD Tree、DocValues── について、検索処理の中での役割を整理します。第1章で見た役割分担を踏まえ、本章では辞書・読み飛ばし・空間分割・圧縮の仕組みを見ていきます。

本章では基本的な役割分担を説明します。実際の検索では、フィールド型や設定、検索条件に応じて、これらの構造が組み合わせて使われます。

## 2.1 Posting List── 語から始まる索引構造

語に基づく検索では、「どの語が、どの文書にあるか」を調べます。Posting List は、ある語を含む文書の `docID` の一覧で、転置インデックス（Inverted Index）を構成する要素です。

ここでいう語は、検索用の単位である term を指します。単語だけでなく、商品コードなどの値全体を一つの語として扱う場合もあります。`docID` と `_id` の違いは、第1章で説明した通りです。

### 2.1.1 語に基づく docID の絞り込み

`term` や `match` による語の検索では、検索する語に対応する posting list を辿り、該当する `docID` を探します。これが語による絞り込みの基本的な仕組みです。

`term` は指定した語をそのまま検索し、`match` は検索文字列を analyzer（文字列を検索用の語に加工する仕組み）で処理して検索します。複数の条件があるときは、それぞれの条件を組み合わせて一致する文書を判断します。

### 2.1.2 転置インデックスの物理構造

転置インデックスは、大きく次の要素に分けて理解できます。

- `Term Dictionary`：フィールドに現れる語を整理し、検索する語を探すための辞書
- `Postings`：各語を含む `docID` の一覧。設定によって、語の出現回数や位置なども保持します

語を探す際は、辞書で対象語を見つけ、その語に紐づいた posting list を参照します。

> Lucene の BlockTree という実装では、語をブロックにまとめて保存し、FST（文字列をコンパクトに扱う索引）を使って該当するブロックへ到達します。理解の要点は「語を探す辞書」と「その語を含む文書の一覧」を分けることです。細かな保存形式は実装バージョンによって変わります。

`text` の辞書に登録される語は analyzer の処理結果です。分かち書きや正規化の設定によって、どの語が一致するかも変わります。

### 2.1.3 skip list による高速化とその制限

Posting List の `docID` は順序を持っています。Lucene は skip list などの読み飛ばす仕組みを使い、必要な番号まで途中を一件ずつ確認せずに進めるようにしています。

ただし、一致する文書が非常に多い場合は、その分の処理も必要です。読み飛ばす仕組みがあることと、どの検索でも同じ速度で返ることは分けて考えましょう。

### 2.1.4 `text`と`keyword`の違い

- `text` フィールドは analyzer によりトークン化され、各語を索引します。全文検索向きです。
- `keyword` フィールドは値全体を一つの語として扱います。コードやカテゴリの完全一致による絞り込みなどに向いています。

例：

- `text` の場合："lorem ipsum ..." → "lorem", "ipsum" などに分解
- `keyword` の場合："lorem ipsum" → "lorem ipsum"（一つの語として扱う）

この違いが、辞書に入る語の単位を決めます。各型の用途や既定の構造の組み合わせは、第3章で整理します。

### 2.1.5 `boolean`型や配列型との相性

通常の索引設定では、OpenSearch の `boolean` も true / false を語として索引し、値の一致で絞り込めます。

配列の扱いは、要素の型によります。たとえば `keyword` フィールドに `["赤", "青"]` を登録すると、それぞれの値を語として索引し、「赤が含まれる」という条件で検索できます。数値の配列なら、数値用の構造で扱います。

オブジェクト配列で、同じ要素内の属性の対応を検索したい場合には、別の判断が必要です。`object` と `nested` の違いは第6章で説明します。

---

## 2.2 BKD Tree── 数値と空間を扱う構造

数値や日付、座標の範囲検索を支える代表的な構造が BKD Tree です。値の空間を分割し、検索条件に合わない領域を読み飛ばして絞り込みます。

### 2.2.1 範囲条件に対する絞り込み

「価格が1000円以上」「2023年1月以降のデータ」といった条件では、数値や `date` として索引された値を範囲で検索します。通常の索引設定では、BKD Tree がこの処理を支えます。

ただし、実行方法は設定や他の条件にも依存します。DocValues を使って値を確認する場合もあり、クエリ名だけで使う構造が一つに決まるわけではありません。

### 2.2.2 空間を再帰的に分割する構造

BKD Tree は、k-d tree に基づく空間分割の仕組みです。値の空間を繰り返し分割し、末端のブロックに値と `docID` をまとめます。

検索時には領域の境界と条件を比較し、条件に合わない領域を読み飛ばします。領域全体が条件に入る場合には、個々の値を調べる処理を省けます。

処理量は検索範囲、一致する件数、値の分布などによって変わります。狭い範囲を効率よく絞れても、ほぼすべての文書が一致する広い範囲では、多くの文書を扱う必要があります。

### 2.2.3 クエリと実行効率

数値・日時の `range`、座標の `geo_bounding_box` や `geo_distance` などの検索では、BKD Tree が条件に合う領域を絞るために使われます。

BKD Tree の利点は、数値や座標の範囲に合わせて不要な領域を読み飛ばせることです。応答時間は、条件の広さや一致件数、他の条件との組み合わせにも依存します。設計時には、実際に使う範囲条件で確認しましょう。

### 2.2.4 数値や座標を多次元で扱う

通常の索引設定では、`long`、`double`、`date`、`geo_point` などの値を、比較できる数値の形に変換して BKD Tree に格納します。

- `geo_point` は緯度・経度の **2次元** の値として扱います。
- `long` や `date` は **1次元** の値として扱い、範囲検索に使います。

### 2.2.5 `date` 型と Lucene の実際の型

入力JSONの書き方と、検索用のフィールド型は区別します。たとえば `"2024-05-01"` という文字列でも、フィールドを `date` として定義していれば、OpenSearch は指定した日付形式で解析して日時として扱います。

通常の `date` は、内部ではエポックミリ秒（1970年1月1日 UTC からのミリ秒数）を表す整数になります。Lucene では、この数値の範囲として日時を検索できます。より細かい時刻を扱う `date_nanos` は、ナノ秒単位の整数を使います。

ここでは、入力形式を解析して内部の比較可能な値に変換する点を押さえてください。型の選び方と、数値を文字列として扱う場合の注意点は、第3章で説明します。

### 脚注

BKD Tree の空間分割とブロック構造については、[Lucene 10.2.1 `org.apache.lucene.util.bkd` の公式Javadoc](https://lucene.apache.org/core/10_2_1/core/org/apache/lucene/util/bkd/package-summary.html)を参照してください。同ページから、実装の背景となる論文も参照できます。

---

## 2.3 DocValues: 値を取り出すためのストレージ構造：docID → 値

第1章で説明した「docID → 値」の参照を、DocValues はフィールドごとにまとめた構造で支えます。たとえば価格の集計なら、必要な文書の価格を、価格の列から読み取るイメージです。

> フィールドごとに値をまとめて保持する列指向の構造については、[Lucene 10.2.1 `org.apache.lucene.index` パッケージ解説](https://lucene.apache.org/core/10_2_1/core/org/apache/lucene/index/package-summary.html)を参照してください。

### 2.3.2 差分圧縮・bit packing による省メモリ設計

DocValues は、同じフィールドに属する値をまとめて保存する性質を活かして圧縮します。値の型や分布、保存形式に応じて、次のような技術を使います。

- 差分圧縮（delta encoding）：基準となる値との差などを保存します。
- 固定ビット幅圧縮（bit packing）：必要なビット数に合わせて値を詰めて保存します。

圧縮の細かな処理は Lucene に任せられます。フィールド型が定める数値の範囲や精度とは別の、保存形式上の工夫です。

### 2.3.3 DocValues の設計対象となるフィールド

DocValues を持つ型や既定設定、集計・ソート・値の取得に合わせた設定の選び方は、第3章で整理します。本章では、フィールドごとに値をまとめて保存する構造と、次節の実行時の使われ方を押さえましょう。

> 保存構造に関する補足として、現在の OpenSearch には DocValues や stored fields（個別に保存したフィールド値）から `_source` を再構成する derived source もあります。再構成した配列の順序や重複などが元のJSONと異なる場合があります。通常の `_source` の役割は第3章で説明します。

### 2.3.4 絞り込みにも使われる DocValues

DocValues の主な役割は、文書から値を読むことです。一方、読み取った値が条件に合うかを調べることで、検索の絞り込みにも使えます。

たとえば、別の条件ですでに少数の候補に絞れている場合、その候補の価格を DocValues から読み、範囲内かを確認する方法が効率的なことがあります。Lucene は、索引を使う方法と DocValues を使う方法を、条件に応じて選択する仕組みを持っています。

OpenSearch 3.2 では、DocValues の範囲検索などを助ける `skip_list` 設定も導入されました。補助索引を使い、条件に合わないドキュメントの範囲を読み飛ばす仕組みです。2.1.3節の Posting List の読み飛ばしとは、対象となる構造が異なります。

基本の役割分担を理解したうえで、実際の検索では構造を組み合わせて最適化する、と捉えましょう。

---

次章では、これらの主要な構造を踏まえ、検索・集計・取得の目的に合わせて OpenSearch のフィールド型や設定を選ぶ設計パターンを説明します。

## 参考資料

- [Lucene 10.2.1：BlockTree の語辞書と索引](https://lucene.apache.org/core/10_2_1/core/org/apache/lucene/codecs/lucene90/blocktree/Lucene90BlockTreeTermsWriter.html)
- [Lucene 10.2.1：BKD Tree](https://lucene.apache.org/core/10_2_1/core/org/apache/lucene/util/bkd/package-summary.html)
- [Lucene 10.2.1：DocValues を使う検索](https://lucene.apache.org/core/10_2_1/core/org/apache/lucene/search/IndexOrDocValuesQuery.html)
- [OpenSearch：date](https://docs.opensearch.org/latest/mappings/supported-field-types/date/)
- [OpenSearch：date_nanos](https://docs.opensearch.org/latest/mappings/supported-field-types/date-nanos/)
- [OpenSearch：DocValues](https://docs.opensearch.org/latest/mappings/mapping-parameters/doc-values/)
- [OpenSearch：_source と derived source](https://docs.opensearch.org/latest/mappings/metadata-fields/source/)
- [OpenSearch：3.2 の skip_list 導入](https://opensearch.org/blog/introducing-opensearch-3-2-next-generation-search-and-anayltics-with-enchanced-ai-capabilities/)
