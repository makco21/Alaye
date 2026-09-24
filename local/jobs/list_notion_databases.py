"""Integration がアクセスできる Notion データベースを一覧表示する CLI。"""

from typing import Any

from packages.integrations.notion.src.client import search_databases


def database_title(database: dict[str, Any]) -> str:
    """Notion database のタイトルを表示用文字列へ変換する。"""

    title = database.get("title", [])
    return "".join(item.get("plain_text", "") for item in title) or "Untitled"


def main() -> None:
    """アクセス可能なデータベースの ID とタイトルを表示する。"""

    databases = search_databases()
    print(f"Databases found: {len(databases)}")
    for database in databases:
        print(f"- {database['id']}: {database_title(database)}")


if __name__ == "__main__":
    main()