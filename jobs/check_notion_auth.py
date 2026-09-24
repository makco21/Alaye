"""Notion の認証状態を確認する CLI。"""

from packages.integrations.notion.src.auth import verify_notion_authentication


def main() -> None:
    """認証済み integration の公開情報だけを表示する。"""

    identity = verify_notion_authentication()
    print(f"Notion authentication succeeded: {identity.name or identity.id}")


if __name__ == "__main__":
    main()