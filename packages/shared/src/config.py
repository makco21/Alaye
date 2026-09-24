"""アプリケーション設定を環境変数から読み込む。"""

from dataclasses import dataclass
import os


class ConfigurationError(ValueError):
    """必須設定が不足している場合に送出する。"""


@dataclass(frozen=True)
class Settings:
    """外部サービス接続に必要な設定。"""

    notion_token: str
    notion_version: str = "2022-06-28"


def load_settings() -> Settings:
    """環境変数を検証して設定を返す。"""

    notion_token = os.getenv("NOTION_TOKEN", "").strip()
    if not notion_token:
        raise ConfigurationError("NOTION_TOKEN is required")

    notion_version = os.getenv("NOTION_VERSION", "2022-06-28").strip()
    return Settings(notion_token=notion_token, notion_version=notion_version)