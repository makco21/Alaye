# Alaye

Alaye は、Notion を情報の正本とし、カレンダーや日常の記録を一つの作業フローで扱うことを目的にしたプロジェクトです。

現在のコードベースは「設計・骨格・Notion 接続の基盤」が整っており、実際に動く部分と未実装の部分が分かれている状態です。特に、環境設定と Notion 認証確認は実装済みで、それ以外の API/ユースケース/同期処理は段階的に拡張中です。

## 現在の実装状況

### 実装済み

- `packages/shared/src/config.py`
  - `.env` / 環境変数から設定を読み込むロジック
  - `NOTION_TOKEN` を必須として扱う
  - Notion のデータベース ID を複数環境変数として受け取る
- `packages/integrations/notion/src/auth.py`
  - `notion_client` を生成する
  - `users.me()` でトークンの認証を確認する
- `jobs/check_notion_auth.py`
  - 認証チェック用 CLI
- `jobs/list_notion_databases.py`
  - Integration がアクセス可能なデータベース一覧の確認
- `jobs/read_records.py`
  - 取得した Records を簡単に読み取る CLI

### まだ未実装/プレースホルダー

- `apps/api/src/main.py`
  - HTTP API のエントリーポイントとして TODO のまま
- `apps/api/src/routes/*.py`
  - records / tasks / calendar / sync の各エンドポイントが未実装
- `packages/application/*`
  - Records / Tasks / Sync の実務処理が未実装
- `packages/persistence/*`
  - 永続化層の実装が未完了
- Web フロントの実装 (`apps/web/src/index.ts`) はまだ土台段階

このため、README は「プロジェクトの方向性」と「現在利用可能なセットアップ」を明確に書くことが重要です。

## 目標と設計方針

- 記録・タスク・プロジェクト情報は Notion を source of truth とする
- 予定はカレンダーと同期し、時間軸で見られるようにする
- 外部 API 呼び出しはアプリケーション層から切り離す
- 同期は冪等性を持ち、失敗時に再実行できるようにする
- Web UI は TypeScript、バックエンドと連携層は Python で実装する

詳細な設計の意図とディレクトリ方針は [docs/project-structure.md](docs/project-structure.md) を参照してください。

## プロジェクト構成

```text
Alaye/
├── apps/
│   ├── api/
│   │   └── src/
│   │       ├── main.py          # TODO: API 起動エントリーポイント
│   │       ├── dependencies.py
│   │       └── routes/
│   │           ├── calendar.py
│   │           ├── records.py
│   │           ├── sync.py
│   │           └── tasks.py
│   └── web/
│       └── src/
│           └── index.ts
├── packages/
│   ├── application/
│   │   └── src/
│   │       ├── record_views.py
│   │       ├── records.py
│   │       ├── sync.py
│   │       └── tasks.py
│   ├── domain/
│   │   └── src/
│   │       ├── models.py
│   │       └── rules.py
│   ├── integrations/
│   │   ├── calendar/
│   │   └── notion/
│   │       └── src/
│   │           ├── auth.py
│   │           ├── client.py
│   │           └── mapper.py
│   ├── persistence/
│   │   └── src/
│   │       ├── models.py
│   │       └── repositories.py
│   └── shared/
│       └── src/
│           └── config.py
├── jobs/
│   ├── check_notion_auth.py
│   ├── list_notion_databases.py
│   ├── read_records.py
│   ├── reconcile.py
│   ├── sync_calendar.py
│   └── sync_notion.py
├── db/
│   ├── migrations/
│   └── seed/
├── docs/
│   └── project-structure.md
├── .env
├── requirements.txt
├── README.md
└── .env.example (任意のテンプレート)
```

## 依存関係

```bash
pip install -r requirements.txt
```

現在の依存は次の通りです。

```text
notion-client>=2.2.1,<3.0.0
python-dotenv>=1.0.0,<2.0.0
```

## 環境変数の設定

ローカル実行時は `.env` または OS 環境変数に次の値を設定してください。

```bash
NOTION_TOKEN=your_integration_token
NOTION_VERSION=2022-06-28

# 基本データベース
NOTION_RECORDS_DATABASE_ID=
NOTION_TASKS_DATABASE_ID=
NOTION_PROJECTS_DATABASE_ID=
NOTION_AREAS_DATABASE_ID=

# 追加/既存の個別データベース
NOTION_CL250_DATABASE_ID=
NOTION_MAINTENANCE_RECORDS_DATABASE_ID=
NOTION_MAINTENANCE_PROJECTS_DATABASE_ID=
NOTION_MY_TASKS_DATABASE_ID=
NOTION_UNTITLED_DATABASE_ID=
NOTION_PEOPLE_DATABASE_ID=
NOTION_MORNING_DATABASE_ID=
NOTION_KEYWORDS_DATABASE_ID=
```

> `.env` はローカル設定ファイルとして使用し、実際のシークレット値をコミットしないでください。

## Notion 認証確認

1. Notion で Internal Integration を作成する
2. 利用する Records / Tasks / Projects などのデータベースを Integration に共有する
3. `NOTION_TOKEN` を設定する
4. 次のコマンドを実行する

```bash
python -m jobs.check_notion_auth
```

このコマンドはトークンそのものを出力せず、接続先の Notion bot の公開情報を表示します。

## データベース一覧の確認

Notion の Database ID が不明な場合は次を実行します。

```bash
python -m jobs.list_notion_databases
```

表示された ID を `NOTION_RECORDS_DATABASE_ID` などに設定してから、以下で実際にデータを読み取れます。

```bash
python -m jobs.read_records
```

## CL250 过期项目导出到日历

`CL250` 数据库中状态为 `已过期` 的项目，可以导出成 Google Calendar / Apple Calendar 可直接使用的格式。

```bash
python jobs/export_cl250_expired_projects.py --format google
python jobs/export_cl250_expired_projects.py --format google --append-to-google
python jobs/export_cl250_expired_projects.py --format apple
python jobs/export_cl250_expired_projects.py --format json
```

- `google`: 输出 Google Calendar API 可直接使用的 JSON 事件列表
- `google --append-to-google`: 通过 OAuth 追加到 Google Calendar，默认日历为 `primary`
- `apple`: 输出 Apple Calendar 可导入的 ICS 内容
- `json`: 纯 JSON，便于调试或二次加工

导出逻辑会读取 `NOTION_CL250_DATABASE_ID` 对应的数据库，并过滤状态为已过期的项目，生成带标题、日期和描述的事件对象。

使用 Google 追加功能前，请在项目根目录放置 Google OAuth 桌面应用凭据 `credentials.json`。首次运行会打开授权页面，并将刷新令牌保存为 `token.json`；也可以通过 `--calendar-id`、`--google-credentials` 和 `--google-token` 覆盖默认值。

## 今後の開発計画

1. Notion のデータベース設計と API 接続の確認
2. Records / Tasks / Projects の読み取りロジックを実装
3. API と Web 画面の最小構成を作成
4. カレンダー同期と差分同期の仕組みを実装
5. 再実行・競合解消・監査ログの導入

## 参考資料

- [docs/project-structure.md](docs/project-structure.md)
- [apps/api/src/main.py](apps/api/src/main.py)
- [packages/shared/src/config.py](packages/shared/src/config.py)
- [packages/integrations/notion/src/auth.py](packages/integrations/notion/src/auth.py)

現在の実装は「設計と基礎の準備」が中心で、プロダクトとして動かすにはさらに API 層とドメイン・永続化の実装が必要です。
