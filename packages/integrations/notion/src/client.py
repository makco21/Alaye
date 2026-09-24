"""Notion API の薄いクライアント。"""

from typing import Any

from .auth import create_notion_client


def get_notion_client() -> Any:
	"""環境変数から構成した Notion クライアントを返す。"""

	return create_notion_client()


# TODO: rate limit、ページ・データベースの取得と更新を実装する。
# TODO: Notion 固有のレスポンスを application 層へ直接公開しない。
