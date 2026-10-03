# 第10章：物理設計

## 10.1 仕組みの理解（土台）
	•	ノードの役割
	•	Data / Master（Cluster-manager）/ Coordinator / Ingest
	•	兼任と専任のトレードオフ（少数構成 vs 中規模以上）
	•	データ構造
	•	シャード（primary/replica、routing の基本）
	•	Lucene セグメントと merge プロセス（I/O・CPU・メモリへの影響）
	•	translog / commit / refresh / flush の関係
	•	検索・書き込みのパイプライン
	•	Ingest → 索引 → refresh → 検索（near-real-time）
	•	Coordinator の scatter/gather と reduce

## 10.2 ノード設計（役割と台数設計）
	•	原則：「全ては役割」— 負荷の発生源を分離する
	•	役割別ガイド
	•	Master：奇数台（3/5/7…）で quorum、GC 安定性
	•	Data：スケールアウト前提、HA は最低2台以上（ゾーン分散）
	•	Coordinator：検索 reduce のオフロード基準（P95 レイテンシ/CPU）
	•	Ingest：パイプライン内容（grok/geoIP/スクリプト）とスループット見積
	•	典型構成パターン
	•	小規模（3 台）/ 中規模（6–9 台）/ 大規模（専任役割＋ゾーン3）
	•	リソース見積もり
	•	CPU/メモリ/ディスク/ネットワークのボトルネック解析
	•	JVM ヒープと OS ページキャッシュのバランス指針

## 10.3 インデックス設計（シャード・レプリカ・ライフサイクル）
	•	シャード設計
	•	適正シャード数/サイズの目安（ターゲット 10–50GB などの方針）
	•	routing（_id / custom routing）とホットキー対策
	•	replica 数の動的調整（書き込み中は 0→安定後に増やす等）
	•	テンプレート/エイリアス
	•	書き込みエイリアス（is_write_index）でのゼロダウン切替
	•	インデックス命名規則（time-series/業務単位）
	•	ライフサイクル
	•	rollover / force-merge / read-only / close / delete
	•	Snapshot/SLM と復旧設計（RPO/RTO の決め方）

## 10.4 更新設計（書き込みの物理チューニング）
	•	Bulk が正義：スループット最大化の基本
	•	バッチサイズ/同時実行/再試行戦略/バックプレッシャ
	•	refresh_interval / index.buffer / merge ポリシ
	•	“小さな書き込みたくさんはNG” を数値で回避する
	•	部分更新・Upsert の注意
	•	version/conflict、外部ロック vs 楽観ロック
	•	スクリプト更新のコストと代替（整流パイプライン）

## 10.5 検索性能設計（クエリ側の物理）
	•	キャッシュ戦略
	•	query cache / request cache / fielddata の使い分け
	•	集計（aggregation）と doc_values の関係
	•	フィルタ設計とプリヒート
	•	filter context、ビットセット、よく使う条件の再利用
	•	ソート/集計の物理負荷
	•	メモリと一時領域、段階的集計（composite など）選択基準

## 10.6 配置と耐障害性（アロケーション設計）
	•	ゾーン/ラック感度（allocation awareness / filtering）
	•	ディスク水位（low/high/flood-stage）と自動再配置
	•	リバランスとクラスター安定化のパラメータ
	•	再投入時のスロットリング（recovery/max_bytes_per_sec 等）

## 10.7 ストレージと I/O（ディスク設計）
	•	媒体選定（NVMe/SATA/ネットワークストレージ）の指針
	•	スループット vs IOPS、ファイルシステムとマウントオプション
	•	スナップショットリポジトリ（S3/NFS）と帯域管理

## 10.8 メモリと JVM（ヒープ/GC/ブレーカー）
	•	ヒープサイズの決め方（OS キャッシュとの分配）
	•	GC ポリシと観測（STW 影響/若年代比率）
	•	Circuit breaker と OOM 防止（集計/スクリプト/フィールドデータ）

## 10.9 運用監視と SLO（守りの設計）
	•	主要メトリクス
	•	indexing/search latency（P50/P95）、merge time、segment 数
	•	heap 使用率、GC pause、I/O 待ち、スロットリング
	•	ダッシュボードとアラート閾値の設計
	•	キャパシティプランニング（成長率/シャード寿命/ロールオーバ周期）

## 10.10 メンテナンス動作（無停止の再配置と最適化）
	•	shrink/split/reindex の安全手順
	•	force-merge の使い所とやってはいけないタイミング
	•	ロールオーバ＋エイリアスでのゼロダウン変更

## 10.11 失敗モードと復旧設計
	•	ノードダウン/ディスク満杯/ネット分断（分割脳）シナリオ
	•	スナップショットからの段階復旧（優先順序と検証手順）
	•	誤更新・誤削除への対処（DLQ 相当の外部保全/監査ログ）

## 10.12 物理設計チェックリスト（配布用）
	•	小規模/中規模/大規模での推奨既定値セット
	•	本番前レビュー項目（シャード、エイリアス、ISM/ILM、監視、DR）