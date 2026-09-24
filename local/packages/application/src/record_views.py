"""Records の View ごとの Notion query 条件。"""

from typing import Any, TypedDict


class RecordView(TypedDict, total=False):
    """Records View に指定できる query 条件。"""

    filter: dict[str, Any]
    sorts: list[dict[str, Any]]


RECORD_VIEWS: dict[str, RecordView] = {
    "all": {
        "sorts": [
            {
                "timestamp": "last_edited_time",
                "direction": "descending",
            }
        ],
    },
    "recent": {
        "filter": {
            "timestamp": "last_edited_time",
            "last_edited_time": {"past_week": {}},
        },
        "sorts": [
            {
                "timestamp": "last_edited_time",
                "direction": "descending",
            }
        ],
    },
}


def get_record_view(view_name: str) -> RecordView:
    """指定された Records View の設定を返す。"""

    try:
        return RECORD_VIEWS[view_name]
    except KeyError as error:
        available_views = ", ".join(sorted(RECORD_VIEWS))
        raise ValueError(
            f"Unknown Records view '{view_name}'. Available views: {available_views}"
        ) from error