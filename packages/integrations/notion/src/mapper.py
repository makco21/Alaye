"""Notion のページ・プロパティとドメインモデルの変換。"""

from typing import Any

from packages.domain.src.models import Record


def property_value(property_data: dict[str, Any] | None) -> Any:
	"""Notion property の型をアプリケーションで扱える値へ変換する。"""

	if not property_data:
		return None

	property_type = property_data.get("type")
	if property_type in {"title", "rich_text"}:
		return "".join(item.get("plain_text", "") for item in property_data.get(property_type, []))
	if property_type in {"select", "status"}:
		selected = property_data.get(property_type)
		return selected.get("name") if selected else None
	if property_type == "multi_select":
		return [item.get("name", "") for item in property_data.get(property_type, [])]
	if property_type == "date":
		date_value = property_data.get("date")
		return date_value.get("start") if date_value else None
	if property_type == "relation":
		return [item.get("id") for item in property_data.get("relation", [])]
	if property_type == "people":
		return [item.get("name") or item.get("id") for item in property_data.get("people", [])]
	return property_data.get(property_type)


def page_to_record(page: dict[str, Any]) -> Record:
	"""Notion page を Record ドメインモデルへ変換する。"""

	properties = page.get("properties", {})
	related_task = property_value(properties.get("RelatedTask"))
	if isinstance(related_task, list):
		related_task = related_task[0] if related_task else None

	return Record(
		id=page["id"],
		title=property_value(properties.get("Title")) or "Untitled",
		record_type=property_value(properties.get("Type")),
		recorded_at=property_value(properties.get("RecordedAt")),
		project=property_value(properties.get("Project")),
		tags=property_value(properties.get("Tags")) or [],
		related_task=related_task,
		calendar_event_id=property_value(properties.get("CalendarEventId")),
		url=page.get("url"),
		last_edited_time=page.get("last_edited_time"),
	)
