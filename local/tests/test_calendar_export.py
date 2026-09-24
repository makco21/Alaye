from packages.integrations.calendar.src.mapper import build_google_calendar_event
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


def test_query_database_supports_new_data_source_api():
    pages = query_database("db-123", client=FakeNotionClient())
    assert len(pages) == 1
    assert pages[0]["id"] == "page-1"


def test_build_google_calendar_event_from_expired_project():
    page = {
        "id": "page-1",
        "url": "https://example.com/p1",
        "properties": {
            "Title": {"title": [{"plain_text": "项目A"}]},
            "Status": {"status": {"name": "已过期"}},
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
