# 本文の実機検証

OpenSearch 3.9.0 + analysis-kuromoji の専用環境です。検証用コンテナだけを起動し、既存環境には接続しません。Security plugin を無効にしているため、compose の公開先をループバックから変更しないでください。

```sh
docker --context desktop-linux compose -f verification/compose.yaml up -d --build
```

起動後、http://127.0.0.1:19200/ が応答することを確認して実行します。

```sh
python3 verification/run.py
```

run.py は毎回別の lbv- 接頭辞のインデックスを作ります。本文が別の場所にある場合は BOOK_ROOT でディレクトリを指定できます。結果・リクエスト応答はスクリプトと同じ場所へ保存します。単一ノードの検証データを使い、性能測定にはしません。

Lucene の直接検証：

```sh
docker --context desktop-linux cp verification/LuceneProbe.java lucene-book-verification-20261003:/tmp/LuceneProbe.java
docker --context desktop-linux exec lucene-book-verification-20261003 /usr/share/opensearch/jdk/bin/java --enable-native-access=ALL-UNNAMED --add-modules jdk.incubator.vector --class-path '/usr/share/opensearch/lib/*' /tmp/LuceneProbe.java
```

検証後の停止：

```sh
docker --context desktop-linux compose -f verification/compose.yaml stop
```

今回の結果は REPORT.md、章・節の一覧は verification-plan.md を参照してください。initial-* と recheck.py / supplement.py は今回の調査・再確認の履歴です。通常の再実行には run.py の60項目と LuceneProbe.java を使います。最初のエラー結果も、本文の訂正に至った証跡として残しています。

記録中のローカルファイルのパスは、リポジトリのルートを基準とする相対パスに統一しています。`chapter-inputs.json` のハッシュは検証時点の本文を示します。過去のエラー記録はファイルのパス表記だけを変更し、検証結果を保持しています。
