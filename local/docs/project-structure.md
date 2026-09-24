# プロジェクト構成

## 1. 全体像

Alaye は、Notion を業務・生活情報の記録基盤として利用し、カレンダーを時間管理の表示・入力基盤として利用します。

```text
Web UI / CLI
    |
Application services
    |-- Records      記録・日報・議事録
    |-- Tasks        タスク・ステータス・期限
    |-- Calendar     予定・時間帯・参加者
    |-- Sync         外部サービス間の同期と再実行
    |
Integration adapters
    |-- Notion API
    |-- Calendar API (Google Calendar 等)
    |
Persistence
    |-- Sync state / idempotency keys / audit logs
```

### データの責務

| データ | 正とする場所 | 役割 |
| --- | --- | --- |
| 記録、タスク、プロジェクト | Notion | 内容、状態、関連情報を保持 |
| 予定の日時、繰り返し、招待 | カレンダー | 時間軸と通知を管理 |
| 外部 ID、同期状態、エラー | Alaye の永続層 | 同期を安全に再実行 |

## 2. 推奨ディレクトリ

```text
.
├── apps/
│   ├── web/
│   │   └── src/index.ts       # TypeScript: 今日の画面、記録、タスク、カレンダー
│   └── api/
│       └── src/
│           ├── main.py        # Python: API 起動とルート登録
│           ├── dependencies.py
│           └── routes/         # records.py, tasks.py, calendar.py, sync.py
├── packages/
│   ├── domain/                 # Python: models.py, rules.py
│   ├── application/            # Python: records.py, tasks.py, sync.py
│   ├── integrations/
│   │   ├── notion/             # Python: auth.py, client.py, mapper.py
│   │   └── calendar/           # Python: client.py, mapper.py
│   ├── persistence/            # Python: repositories.py, models.py
│   └── shared/                 # Python: logger、日時、エラー、設定スキーマ
├── jobs/
│   ├── check_notion_auth.py    # Notion 認証の確認
│   ├── sync_notion.py          # Notion -> Alaye の取り込み
│   ├── sync_calendar.py        # カレンダー -> Alaye の取り込み
│   └── reconcile.py            # 差分解消と失敗ジョブの再実行
├── db/
│   ├── migrations/
│   └── seed/
├── docs/
│   ├── project-structure.md
│   ├── notion-schema.md
│   └── sync-policy.md
├── .env
└── README.md
```

## 3. Notion データベース

最初は次の 4 つに限定します。

### `Records`

日報、メモ、議事録、振り返りを保存します。

`Title`, `Type`, `RecordedAt`, `Project`, `Tags`, `RelatedTask`, `CalendarEventId`

### `Tasks`

実行単位の仕事を保存します。

`Title`, `Status`, `Priority`, `DueDate`, `Project`, `Assignee`, `CalendarEventId`

### `Projects`

目的と関連する記録・タスクをまとめます。

`Name`, `Status`, `StartDate`, `TargetDate`, `Area`, `RepositoryUrl`

### `Areas`

継続的に管理する領域を定義します。

`Name`, `Status`, `ReviewDay`

Notion 固有の page ID、database ID、URL は表示用タイトルと分けて保存し、外部キーとして扱います。

## 4. 主要画面

- `Today`: 当日の予定、期限が近いタスク、今日作成した記録を時系列で表示
- `Records`: 記録の検索・絞り込み・新規作成
- `Tasks`: 状態、期限、プロジェクトの一覧とカレンダー予定の作成
- `Calendar`: 週・月表示と Notion 関連ページへの導線
- `Sync status`: 最終同期、成功・失敗件数、再実行、エラー詳細

最初に `Today` と `Sync status` を作ると、各サービスを横断する価値と連携状態を早期に確認できます。

## 5. 同期ルール

1. Webhook が利用できる場合は受信し、一定間隔の pull をフォールバックにする
2. 取り込み前に外部 ID と更新日時を確認する
3. 同期キーを `provider + externalId + resourceType` として重複作成を防ぐ
4. 更新競合は自動上書きせず、競合状態として記録する
5. rate limit、認証エラー、対象削除を別のエラー種別で保存する
6. 失敗した単位だけを再実行できるようにする

### 初期の書き込み方針

- Records の本文・タグ: Notion が正
- Tasks の状態・期限: Notion が正
- Calendar の日時・繰り返し・参加者: カレンダーが正
- 関連 ID と同期メタデータ: Alaye が管理

## 6. 永続層の最小モデル

```text
external_resources
  id, provider, resource_type, external_id, notion_url, updated_at

sync_cursors
  provider, resource_type, cursor, last_synced_at

sync_runs
  id, provider, started_at, finished_at, status, error_count

sync_conflicts
  id, resource_id, fields, detected_at, resolved_at
```

初期版では Notion 本文を複製せず、ID と同期メタデータだけを保存して二重管理を避けます。

## 7. 実装順序

1. `.env`、Notion integration、対象 database ID の設定
2. Notion adapter と `Records` / `Tasks` の read-only 取得
3. Today 画面の表示と同期ステータス
4. タスク・記録の作成と更新
5. カレンダー adapter と event の関連付け
6. 差分同期、再実行、競合表示
7. 認証、監査ログ、通知、テストの拡充

## 8. 環境変数

秘密情報はリポジトリに置かず、環境変数で管理します。

```text
NOTION_TOKEN=
NOTION_RECORDS_DATABASE_ID=
NOTION_TASKS_DATABASE_ID=
NOTION_PROJECTS_DATABASE_ID=
NOTION_AREAS_DATABASE_ID=
CALENDAR_PROVIDER=google
CALENDAR_CLIENT_ID=
CALENDAR_CLIENT_SECRET=
DATABASE_URL=
```

実装時は起動時に設定を検証し、未設定の連携を画面上で明示的に無効化します。