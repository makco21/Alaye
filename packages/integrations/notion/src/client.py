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
	"""Notion データベースの全ページをページング付きで読み取る。

	Notion SDK の古い `databases.query` と新しい `data_sources.query` の両方に対応する。
	"""

	notion_client = client or get_notion_client()
	results: list[dict[str, Any]] = []
	next_cursor: str | None = None

	try:
		while True:
			query: dict[str, Any] = {"page_size": page_size}
			if filter is not None:
				query["filter"] = filter
			if sorts is not None:
				query["sorts"] = sorts
			if next_cursor:
				query["start_cursor"] = next_cursor

			if hasattr(notion_client, "databases") and hasattr(notion_client.databases, "query"):
				response = notion_client.databases.query(database_id=database_id, **query)
			elif callable(getattr(notion_client, "request", None)):
				try:
					response = notion_client.request(
						path=f"databases/{database_id}/query",
						method="POST",
						body=query,
					)
				except Exception:
					if hasattr(notion_client, "databases") and hasattr(
						notion_client.databases, "retrieve"
					):
						database = notion_client.databases.retrieve(database_id=database_id)
						data_source_id = database.get("data_source_id") or database_id
					else:
						data_source_id = database_id
					response = notion_client.data_sources.query(
						data_source_id=data_source_id,
						**query,
					)
			else:
				if hasattr(notion_client, "databases") and hasattr(notion_client.databases, "retrieve"):
					database = notion_client.databases.retrieve(database_id=database_id)
					data_source_id = database.get("data_source_id") or database_id
				else:
					data_source_id = database_id
				response = notion_client.data_sources.query(data_source_id=data_source_id, **query)

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
