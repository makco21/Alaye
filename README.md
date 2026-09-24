# Alaye

Notion を中心に、日々の記録とカレンダー管理を一つのワークフローで扱うプロジェクトです。

## 方針

- 記録・タスク・プロジェクト情報は Notion を正（source of truth）にする
- 予定はカレンダーと同期し、予定の時間軸を見やすくする
- 外部サービスの API 呼び出しはアプリケーション層から分離する
- 同期処理は冪等にし、失敗時に再実行できるようにする
- Web 画面は TypeScript、API・ドメイン・連携・ジョブは Python で実装する

## プロジェクト構成

設計と実装の境界、推奨ディレクトリ、データモデル、同期フローは [docs/project-structure.md](docs/project-structure.md) にまとめています。

## 想定する段階的な実装

1. Notion のデータベース設計と API 接続確認
2. 記録・タスク・予定を取得して一覧表示
3. カレンダーイベントとの双方向同期
4. 今日のダッシュボード、検索、通知、同期ログを追加

## Notion 認証の確認

1. Notion で Internal Integration を作成し、トークンを発行する
2. 利用する Records / Tasks / Projects データベースを Integration に共有する
3. `NOTION_TOKEN` を環境変数へ設定する
4. `python jobs/check_notion_auth.py` を実行する

SDK の依存関係は `pip install -r requirements.txt` で導入できます。認証確認ではトークンを表示せず、接続先 bot の公開情報だけを表示します。
