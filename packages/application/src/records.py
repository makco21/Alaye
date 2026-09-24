"""記録に関するユースケース。"""

from typing import Any

from packages.domain.src.models import Record
from packages.application.src.record_views import get_record_view
from packages.integrations.notion.src.client import query_database
from packages.integrations.notion.src.mapper import page_to_record
from packages.shared.src.config import ConfigurationError, Settings, load_settings


def list_records(
	view_name: str = "all",
	settings: Settings | None = None,
	client: Any | None = None,
) -> list[Record]:
	"""指定した View 条件で Notion の Records を一覧取得する。"""

	resolved_settings = settings or load_settings()
	database_id = resolved_settings.notion_records_database_id
	if not database_id:
		raise ConfigurationError("NOTION_RECORDS_DATABASE_ID is required")

	view = get_record_view(view_name)
	pages = query_database(
		database_id,
		client=client,
		filter=view.get("filter"),
		sorts=view.get("sorts"),
	)
	return [page_to_record(page) for page in pages]


# TODO: 記録の検索、作成、更新を追加する。
# TODO: 書き込み処理は read-only 取得の動作確認後に実装する。
