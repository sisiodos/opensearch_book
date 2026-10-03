# 著作と再利用に関する方針

本書に含まれる記述（概念構造、設計原則、モデル分類、DSL、図解形式など）は、著者 sisiodos の視点に基づき構成されています。初版の執筆では、一部の章・文章に OpenAI の ChatGPT-4o を補助的に活用しました。今回の改訂では、GPT-6.1 Sol を使用し、改訂時点の公式資料に照らした内容の更新と、検証コードによる実機確認を行っています。

## 著者について

- 構造設計、章立て、概念整理、表現意図の統一は sisiodos が担っています。今回の改訂でも、初学者の理解を優先する編集方針と変更範囲を定め、提案への修正指示と採否の判断を行っています。
- ChatGPT-4o は、初版の草稿生成・文体整形・構造の補助的説明生成に活用されました。
- GPT-6.1 Sol は、今回の本文レビュー、公式資料との照合、修正文案の作成・適用、章間の整合確認、改訂記録の作成を担いました。また、検証項目とコードを作成し、OpenSearch と同梱 Lucene で実行して、結果と証跡を整理しました。
- 著者は sisiodos です。AI は、著者の指示と判断のもとで執筆・改訂・検証に活用しています。

## 再利用について

著者が権利を持つ本書の本文・図・サンプルコード、および付属の検証コードは、別途注記があるものを除き、[MIT ライセンス](#mit-license)で提供します。複製、改変、再配布、商用利用などが可能です。

コピーまたは相当部分を再配布する場合は、MIT ライセンスが定める著作権表示と許諾表示を保持してください。以下のクレジットは読み手に出典を伝えるための推奨表記であり、この条件とは別のものです。

第三者の著作物からの引用、転載した図、外部データやライブラリなどには、それぞれの権利者の利用条件が適用されます。本書のライセンスは、それらへの追加の許諾を与えるものではありません。また、概念・設計原則・用語そのものに独占的な権利を主張する趣旨ではありません。

本書と付属コードは、MIT ライセンスの定めに従い、現状のまま提供します。

### クレジット例

> `sisiodos『Luceneの理解に基づくOpenSearch設計』より`

または、章単位の引用であれば：

> `出典：sisiodos『Luceneの理解に基づくOpenSearch設計』第◯章「〇〇〇」より`

このように明記していただくことで、設計思想が正しく継承され、
知の構造に対する敬意と文脈が未来に残されることを期待しています。

---

## AI を活用した執筆・改訂・検証について

本書は、筆者（sisiodos）が問いと設計意図を示し、AI が説明や修正案を作り、筆者が判断と修正を重ねる対話を通じて、文章・構造・視点を磨いています。初版の ChatGPT-4o と、今回の改訂の GPT-6.1 Sol は、この過程で異なる役割を担っています。本書では、この対話による制作過程を **「意味の共構成」** と呼んでいます。初版で用いた「AI との共著」という表現も、この制作過程を指す呼称です。本文の設計方針と最終的な編集判断は著者が担います。

今回の改訂では、資料による確認に加え、OpenSearch 3.9.0 と同梱 Lucene 10.5.1 で、設定・クエリ・スコア計算などの動作を検証しました。実機で説明との食い違いが見つかった箇所は、結果に合わせて訂正しています。検証は明示した環境とデータでの動作確認であり、本番環境での性能や、すべてのバージョンでの挙動まで確認したものではありません。

章ごとの変更内容は [改訂記録](revisions/)、検証した範囲と結果は [実機検証記録](verification/REPORT.md)、再実行手順は [検証手順](verification/README.md) にまとめています。

読者におかれましては、この文体や構造の背後にある「問い」と「設計意図」にも着目していただければ幸いです。

## MIT License

Zenn で本書を掲載する際にも利用条件を本文内で確認できるよう、著作権表示とライセンス全文を以下に掲載します。再配布時には、この表示を保持してください。

```text
MIT License

Copyright (c) 2025-2026 sisiodos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
