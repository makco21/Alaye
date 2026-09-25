# Alaye 当前环境清单

本文件记录本地开发容器在 2026-09-25 的运行环境快照。秘密值は記載していません。

## システムと Python

| 項目 | 実測値 |
| --- | --- |
| OS | Ubuntu 24.04.5 LTS（コンテナのカーネルは Linux 6.8.0-1064-azure） |
| CPU/arch | x86_64 |
| 作業ディレクトリ | `/workspaces/Alaye` |
| Python | 3.14.2 |
| Python 実体 | `/home/codespace/.python/current/bin/python` |
| pip | 26.2.1 |
| 仮想環境 | `VIRTUAL_ENV` は未設定。システムの Python 3.14 環境を使用 |

## プロジェクト依存

`requirements.txt` に宣言されている範囲と、現在インストールされている実バージョンです。

| パッケージ | 宣言範囲 | 実バージョン | import |
| --- | --- | --- | --- |
| `notion-client` | `>=2.2.1,<3.0.0` | 2.7.0 | OK (`notion_client`) |
| `python-dotenv` | `>=1.0.0,<2.0.0` | 1.2.3 | OK (`dotenv`) |
| `google-api-python-client` | `>=2.149.0,<3.0.0` | 2.200.0 | OK (`googleapiclient`) |
| `google-auth-oauthlib` | `>=1.2.1,<2.0.0` | 1.4.1 | OK (`google_auth_oauthlib`) |

依存検査結果: `python -m pip check` は `No broken requirements found.` でした。

## リポジトリ内の実行確認

| 確認 | 結果 |
| --- | --- |
| Python 構文 | `python -m compileall -q apps jobs packages tests` 成功 |
| 主要外部 import | 4 パッケージすべて成功 |
| pytest | 未導入（`No module named pytest`） |
| Notion 認証 | この清单作成時には未実行 |
| Google Calendar append | `python jobs/export_cl250_expired_projects.py --format google --append-to-google` は終了コード 130。OAuth の対話処理を中断した状態で、依存エラーではない |

## 設定ファイルと環境変数

根目录に `.env` と `credentials.json` が存在します。値はこのファイルに転記しません。

| 項目 | 状態 |
| --- | --- |
| `.env` | 存在。Notion/Google の設定は `python-dotenv` が読み込む |
| `credentials.json` | 存在。Google OAuth デスクトップアプリ資格情報として使用 |
| `NOTION_TOKEN` などの OS 環境変数 | 未設定（名前の検出結果は `PATH` のみ）。`.env` 経由の設定を使用する想定 |
| `token.json` | 現在の根目录一覧では未確認。Google OAuth 初回承認後に生成される |

README に記載されている主な設定名は次の通りです。

```text
NOTION_TOKEN
NOTION_VERSION
NOTION_RECORDS_DATABASE_ID
NOTION_TASKS_DATABASE_ID
NOTION_PROJECTS_DATABASE_ID
NOTION_AREAS_DATABASE_ID
NOTION_CL250_DATABASE_ID
NOTION_MAINTENANCE_RECORDS_DATABASE_ID
NOTION_MAINTENANCE_PROJECTS_DATABASE_ID
NOTION_MY_TASKS_DATABASE_ID
NOTION_UNTITLED_DATABASE_ID
NOTION_PEOPLE_DATABASE_ID
NOTION_MORNING_DATABASE_ID
NOTION_KEYWORDS_DATABASE_ID
```

## インストール済みパッケージのスナップショット

以下は `python -m pip freeze` の実測値です。Jupyter/VS Code 開発環境由来のパッケージも含みます。

```text
anyio==4.15.1
argon2-cffi==25.1.0
argon2-cffi-bindings==26.1.0
arrow==1.4.0
asttokens==3.0.2
async-lru==2.3.0
attrs==26.1.0
babel==2.18.0
beautifulsoup4==4.15.0
bleach==6.4.0
certifi==2026.7.22
cffi==2.1.1
charset-normalizer==3.5.1
colorama==0.4.6
comm==0.2.3
cryptography==50.0.1
debugpy==1.8.21
defusedxml==0.7.1
executing==2.2.1
fastjsonschema==2.22.2
fqdn==1.5.1
gitdb==4.0.12
GitPython==3.1.62
google-api-core==2.38.0
google-api-python-client==2.200.0
google-auth==2.58.0
google-auth-httplib2==0.4.2
google-auth-oauthlib==1.4.1
googleapis-common-protos==1.75.3
h11==0.16.0
httpcore==1.0.9
httplib2==0.32.0
httpx==0.28.1
idna==3.19
ipykernel==7.3.0
ipython==9.17.1
ipython_pygments_lexers==1.1.1
isoduration==20.11.0
jedi==0.20.0
Jinja2==3.1.6
json5==0.15.0
jsonpointer==3.1.1
jsonschema==4.26.0
jsonschema-specifications==2025.9.1
jupyter-events==0.12.1
jupyter-lsp==2.3.1
jupyter_builder==1.2.3
jupyter_client==8.10.0
jupyter_core==5.9.1
jupyter_server==2.21.0
jupyter_server_terminals==0.5.4
jupyterlab==4.6.3
jupyterlab-git-core==0.54.1
jupyterlab_git==0.54.1
jupyterlab_pygments==0.3.0
jupyterlab_server==2.28.0
lark==1.3.1
MarkupSafe==3.0.3
matplotlib-inline==0.2.2
mistune==3.3.4
nbclient==0.11.0
nbconvert==7.17.1
nbdime==4.0.4
nbformat==5.11.1
nest-asyncio2==1.7.2
notebook_shim==0.2.4
notion-client==2.7.0
oauthlib==3.3.1
opentelemetry-api==1.44.0
packaging==26.3
pandocfilters==1.5.1
parso==0.8.7
pexpect==4.9.0
platformdirs==4.11.8
prometheus_client==0.26.0
prompt_toolkit==3.0.53
proto-plus==1.28.4
protobuf==7.36.2
psutil==7.2.2
ptyprocess==0.7.0
pure_eval==0.2.3
pyasn1==0.6.4
pyasn1_modules==0.4.2
pycparser==3.0
Pygments==2.21.0
pyparsing==3.3.3
python-dateutil==2.9.0.post0
python-dotenv==1.2.3
python-json-logger==4.2.0
PyYAML==6.0.3
pyzmq==27.2.0
referencing==0.37.0
requests==2.34.2
requests-oauthlib==2.0.0
rfc3339-validator==0.1.4
rfc3986-validator==0.1.1
rfc3987-syntax==1.1.0
rpds-py==2026.6.3
Send2Trash==2.1.0
six==1.17.0
smmap==5.0.3
soupsieve==2.9.2
stack-data==0.6.3
terminado==0.18.1
tinycss2==1.5.1
tornado==6.5.8
traitlets==5.16.1
typing_extensions==4.16.0
tzdata==2026.3
uri-template==1.3.0
uritemplate==4.2.0
urllib3==2.7.0
wcwidth==0.8.3
webcolors==25.10.0
webencodings==0.6.1
websocket-client==1.9.2
```

## 再現・更新コマンド

同じ Python 実体で実行することが重要です。

```bash
python --version
python -m pip install -r requirements.txt
python -m pip check
python -m compileall -q apps jobs packages tests
python -m pip freeze > pip-freeze.txt
```

pytest を使う場合は、現在の依存定義には含まれていないため、別途インストールが必要です。

```bash
python -m pip install pytest
python -m pytest -q
```