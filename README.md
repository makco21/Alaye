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
4. `python -m jobs.check_notion_auth` を実行する

Records のデータベース ID が分からない場合は、次のコマンドで Integration がアクセスできるデータベースを確認できます。

```bash
python -m jobs.list_notion_databases
```

表示された Records の ID を `NOTION_RECORDS_DATABASE_ID` に設定してから、次のコマンドで内容を読み取ります。

```bash
python -m jobs.read_records
```

SDK の依存関係は `pip install -r requirements.txt` で導入できます。認証確認ではトークンを表示せず、接続先 bot の公開情報だけを表示します。

## Notion データベース設定名

以下の環境変数に、`python -m jobs.list_notion_databases` で確認した各データベースの ID を `.env` に設定します。

| Notion データベース | 環境変数 |
| --- | --- |
| CL250 | `NOTION_CL250_DATABASE_ID` |
| 维护记录 | `NOTION_MAINTENANCE_RECORDS_DATABASE_ID` |
| 维护项目 | `NOTION_MAINTENANCE_PROJECTS_DATABASE_ID` |
| 我的任务 | `NOTION_MY_TASKS_DATABASE_ID` |
| Untitled | `NOTION_UNTITLED_DATABASE_ID` |
| People | `NOTION_PEOPLE_DATABASE_ID` |
| 午前DB | `NOTION_MORNING_DATABASE_ID` |
| キーワードDB | `NOTION_KEYWORDS_DATABASE_ID` |

アプリケーション上の標準用途で参照する場合は、次の共通名も使用します。

| 用途 | 環境変数 |
| --- | --- |
| Records | `NOTION_RECORDS_DATABASE_ID` |
| Tasks | `NOTION_TASKS_DATABASE_ID` |
| Projects | `NOTION_PROJECTS_DATABASE_ID` |
| Areas | `NOTION_AREAS_DATABASE_ID` |

## ディレクトリ
ディレクトリ	役割
domain	業務ルール、ドメインモデル
application	ユースケース、処理の流れ
integrations	Notion・カレンダー API 連携
persistence	DB 保存・取得
shared	設定、ログ、共通エラー
