"""外部サービスに依存しないドメインモデル。"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Record:
	"""Notion の Records ページを表す読み取り専用モデル。"""

	id: str
	title: str
	record_type: str | None = None
	recorded_at: str | None = None
	project: str | None = None
	tags: list[str] = field(default_factory=list)
	related_task: str | None = None
	calendar_event_id: str | None = None
	url: str | None = None
	last_edited_time: str | None = None


# TODO: Task、CalendarEvent、Project の型と不変条件を追加する。
# TODO: 日時はタイムゾーンを含む形式で扱い、外部 API の型を持ち込まない。
