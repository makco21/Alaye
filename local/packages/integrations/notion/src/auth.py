"""Notion API のクライアント生成と認証確認。"""

from dataclasses import dataclass
from typing import Any

from packages.shared.src.config import Settings, load_settings


class NotionAuthenticationError(RuntimeError):
    """Notion API の認証に失敗した場合に送出する。"""


@dataclass(frozen=True)
class NotionIdentity:
    """認証確認で取得した Notion bot の公開情報。"""

    id: str
    name: str | None
    object_type: str
    avatar_url: str | None


def create_notion_client(settings: Settings | None = None) -> Any:
    """設定から Notion SDK のクライアントを生成する。"""

    try:
        from notion_client import Client
    except ImportError as error:
        raise RuntimeError(
            "notion-client is not installed; run 'pip install -r requirements.txt'"
        ) from error

    resolved_settings = settings or load_settings()
    return Client(
        auth=resolved_settings.notion_token,
        notion_version=resolved_settings.notion_version,
    )


def verify_notion_authentication(client: Any | None = None) -> NotionIdentity:
    """Notion の users.me を呼び出し、トークンの有効性を確認する。"""

    notion_client = client or create_notion_client()
    try:
        response = notion_client.users.me()
    except Exception as error:
        raise NotionAuthenticationError(
            "Notion authentication failed. Check NOTION_TOKEN and integration access."
        ) from error

    return NotionIdentity(
        id=response["id"],
        name=response.get("name"),
        object_type=response.get("type", "unknown"),
        avatar_url=response.get("avatar_url"),
    )