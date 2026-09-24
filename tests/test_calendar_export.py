from packages.integrations.calendar.src.mapper import build_google_calendar_event
from packages.integrations.calendar.src.client import build_google_calendar_event_body
from packages.integrations.notion.src.client import query_database


class FakeDataSourcesEndpoint:
    def query(self, data_source_id, **kwargs):
        assert data_source_id == "data-source-123"
        return {
            "results": [{"id": "page-1", "url": "https://example.com/p1"}],
            "has_more": False,
        }


class FakeDatabasesEndpoint:
    def retrieve(self, database_id):
        assert database_id == "db-123"
        return {"id": "db-123", "data_source_id": "data-source-123"}


class FakeNotionClient:
    databases = FakeDatabasesEndpoint()
    data_sources = FakeDataSourcesEndpoint()


class FakeLegacyNotionClient:
    def request(self, path, method, body):
        assert path == "databases/db-123/query"
        assert method == "POST"
        assert body["page_size"] == 100
        return {
            "results": [{"id": "page-1", "url": "https://example.com/p1"}],
            "has_more": False,
        }


def test_query_database_supports_new_data_source_api():
    pages = query_database("db-123", client=FakeNotionClient())
    assert len(pages) == 1
    assert pages[0]["id"] == "page-1"


def test_query_database_supports_legacy_database_api():
    pages = query_database("db-123", client=FakeLegacyNotionClient())
    assert len(pages) == 1
    assert pages[0]["id"] == "page-1"


def test_build_google_calendar_event_from_expired_project():
    page = {
        "id": "page-1",
        "url": "https://example.com/p1",
        "properties": {
            "Title": {"title": [{"plain_text": "项目A"}]},
            "Status": {"status": {"name": "🔴已到期"}},
            "DueDate": {"date": {"start": "2026-09-30"}},
            "Summary": {"rich_text": [{"plain_text": "季度回顾"}]},
        },
    }

    event = build_google_calendar_event(page)

    assert event["summary"] == "项目A"
    assert event["start"] == {"date": "2026-09-30"}
    assert event["end"] == {"date": "2026-10-01"}
    assert event["description"] == "季度回顾"
    assert event["visibility"] == "public"


def test_build_google_calendar_event_from_cl250_properties():
    page = {
        "id": "page-1",
        "properties": {
            "项目": {"title": [{"plain_text": "灯光"}]},
            "状态": {"type": "formula", "formula": {"type": "string", "string": "🔴已到期"}},
            "维护预定日": {"date": {"start": "2026-09-18T21:00:00.000+09:00"}},
            "备注": {"rich_text": [{"plain_text": "需要检查"}]},
        },
    }

    event = build_google_calendar_event(page)

    assert event["summary"] == "灯光"
    assert event["start"] == {"date": "2026-09-18"}
    assert event["description"] == "需要检查"


def test_google_calendar_event_body_uses_only_calendar_fields():
    body = build_google_calendar_event_body(
        {
            "summary": "灯光",
            "description": "需要检查",
            "start": {"date": "2026-09-18"},
            "end": {"date": "2026-09-19"},
            "location": None,
            "visibility": "public",
            "source": {"title": "Notion CL250"},
        }
    )

    assert body == {
        "summary": "灯光",
        "description": "需要检查",
        "start": {"date": "2026-09-18"},
        "end": {"date": "2026-09-19"},
    }
