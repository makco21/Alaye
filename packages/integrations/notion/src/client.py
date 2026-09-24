"""Notion API の薄いクライアント。"""

from typing import Any

from .auth import create_notion_client


class NotionQueryError(RuntimeError):
	"""Notion データベースの取得に失敗した場合に送出する。"""


def get_notion_client() -> Any:
	"""環境変数から構成した Notion クライアントを返す。"""

	return create_notion_client()


def query_database(
	database_id: str,
	client: Any | None = None,
	*,
	filter: dict[str, Any] | None = None,
	sorts: list[dict[str, Any]] | None = None,
	page_size: int = 100,
) -> list[dict[str, Any]]:
	"""Notion データベースの全ページをページング付きで読み取る。"""

	notion_client = client or get_notion_client()
	results: list[dict[str, Any]] = []
	next_cursor: str | None = None

	try:
		while True:
			query: dict[str, Any] = {
				"database_id": database_id,
				"page_size": page_size,
			}
			if filter is not None:
				query["filter"] = filter
			if sorts is not None:
				query["sorts"] = sorts
			if next_cursor:
				query["start_cursor"] = next_cursor

			response = notion_client.databases.query(**query)
			results.extend(response.get("results", []))
			if not response.get("has_more"):
				return results
			next_cursor = response.get("next_cursor")
			if not next_cursor:
				return results
	except Exception as error:
		raise NotionQueryError(
			f"Failed to query Notion database: {database_id}"
		) from error


def search_databases(client: Any | None = None) -> list[dict[str, Any]]:
	"""Integration がアクセスできるデータベースを一覧取得する。"""

	notion_client = client or get_notion_client()
	results: list[dict[str, Any]] = []
	next_cursor: str | None = None

	try:
		while True:
			query: dict[str, Any] = {
				"query": "",
				"filter": {"property": "object", "value": "database"},
				"page_size": 100,
			}
			if next_cursor:
				query["start_cursor"] = next_cursor

			response = notion_client.search(**query)
			results.extend(response.get("results", []))
			if not response.get("has_more"):
				return results
			next_cursor = response.get("next_cursor")
			if not next_cursor:
				return results
	except Exception as error:
		raise NotionQueryError("Failed to search Notion databases") from error


# TODO: rate limit、ページ・データベースの取得と更新を実装する。
# TODO: Notion 固有のレスポンスを application 層へ直接公開しない。
