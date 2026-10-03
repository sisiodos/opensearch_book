# 第8章 改訂記録

改訂日：2026-10-03

第8章では、店舗などの位置を geo_point で表し、距離・矩形・多角形の条件で検索します。座標の順序、検索範囲、距離によるソートとスコア調整を分け、用途から設定を選べるように説明しています。

改訂内容を、用語・説明などの訂正（errata）と、説明の充実・整理や実装バージョンへの対応（revised）に分類しています。

## errata

| 節 | 改訂後の内容 |
| --- | --- |
| 8.1 内部の索引 | geo_point の緯度・経度を2次元の BKD Tree で索引することを説明しています。DocValues による距離ソートや集計も第3章へつなげています。 |
| 8.1 測地系と座標参照系 | WGS84 と、緯度・経度を使う座標参照系 EPSG:4326 を分けて説明しています。 |
| 8.2 入力形式 | 形式を統一する目的を、座標順序の取り違え防止と確認のしやすさとして説明しています。同じ座標の表記を変えても位置の精度が上がるわけではないことを示しています。 |
| 8.3 多角形と行政区域 | 多角形を説明用の範囲として示し、実際の行政区域とは区別しています。国土数値情報の提供元を国土交通省とし、座標参照系の確認・変換を説明しています。 |
| 8.5 点と形状の選択 | geo_point は複数の位置も保持でき、geo_shape は点や線・面などを表せることを示しています。型だけによる一律の速度比較を改めています。 |

## revised

| 節 | 改訂後の内容 |
| --- | --- |
| 8.2 座標の確認 | 文字列の lat,lon と配列の lon,lat を区別し、lat・lon を明示するオブジェクト形式と値の範囲を案内しています。 |
| 8.3 基本クエリ | 距離条件は移動距離や所要時間とは異なることを説明しています。矩形は地図の表示範囲など、用途に合った条件として紹介しています。 |
| 8.3 geo_shape（version update） | 多角形で点を絞る例を現行の公式資料に合わせた geo_shape クエリへ更新しています。対象は geo_point のまま、intersects を使い、GeoJSON の座標順序と外周の閉じ方を説明しています。 |
| 8.4 ソートとスコア | _geo_distance による近い順のソートを短い例で示しています。gauss の scale は検索範囲の上限ではなく減衰の設定として説明しています。 |
| 8.5 型とクエリの関係 | 点を多角形で絞る場合と、形状自体を保持する場合を区別し、フィールド型とクエリ名を分けて選ぶ考え方を示しています。 |

## 参考資料

- [OpenSearch：geo_point](https://docs.opensearch.org/latest/mappings/supported-field-types/geo-point/)
- [OpenSearch：geo_shape](https://docs.opensearch.org/latest/mappings/supported-field-types/geo-shape/)
- [OpenSearch：geoshape query](https://docs.opensearch.org/latest/query-dsl/geo-and-xy/geoshape/)
- [OpenSearch：距離によるソート](https://docs.opensearch.org/latest/search-plugins/searching-data/sort/)
- [OpenSearch：function_score と減衰関数](https://docs.opensearch.org/latest/query-dsl/compound/function-score/)
- [Lucene 10.2.1：LatLonPoint](https://lucene.apache.org/core/10_2_1/core/org/apache/lucene/document/LatLonPoint.html)
- [国土交通省：国土数値情報](https://nlftp.mlit.go.jp/ksj/)

## 今回の更新範囲

第8章の本文に改訂を適用し、その内容に合わせて改訂記録を作成しました。既存の8.1〜8.5の構成、東京駅を中心とする距離検索・矩形・多角形・スコアの例を活かしています。多角形の例は geo_shape クエリへ更新し、距離ソートの例を補っています。初学者が座標と検索条件を理解するための範囲にとどめています。公式資料との照合、JSON と節構成・差分の確認を行いました。境界ケースの網羅検証・性能測定と出版用レンダリングは未実施です。

2026-10-03 の実機検証では、OpenSearch 3.9.0（Lucene 10.5.1）で本章に対応する動作確認4項目が成功しました。対象と前提条件、証跡、未検証範囲は [実機検証記録](../verification/REPORT.md) にまとめています。性能の一般的な保証や出版用レンダリングの確認は含みません。
