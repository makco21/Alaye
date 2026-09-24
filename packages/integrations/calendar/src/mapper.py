"""カレンダーイベントとドメインモデルの変換。"""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

def _property_text(property_data: dict[str, Any] | None) -> str | None:
    """Notion property を文字列へ正規化する。"""

    if not property_data:
        return None

    property_type = property_data.get("type")
    if property_type is None:
        for candidate in ("title", "rich_text", "select", "status", "date", "number"):
            if candidate in property_data:
                property_type = candidate
                break

    if property_type in {"title", "rich_text"}:
        values = property_data.get(property_type, [])
        return "".join(item.get("plain_text", "") for item in values) or None
    if property_type == "formula":
        formula = property_data.get("formula")
        if isinstance(formula, dict):
            formula_type = formula.get("type")
            formula_value = formula.get(formula_type) if formula_type else None
            return str(formula_value) if formula_value is not None else None
        return None
    if property_type in {"select", "status"}:
        selected = property_data.get(property_type)
        if isinstance(selected, dict):
            return selected.get("name")
        return str(selected) if selected is not None else None
    if property_type == "date":
        date_value = property_data.get("date")
        if isinstance(date_value, dict):
            start_value = date_value.get("start")
            return start_value.split("T", 1)[0] if start_value else None
        return None
    if property_type == "number":
        number_value = property_data.get("number")
        return str(number_value) if number_value is not None else None
    return None


def is_expired_project(page: dict[str, Any]) -> bool:
    """CL250 のページが期限切れ状態かを判定する。"""

    properties = page.get("properties", {})
    status_value = _property_text(properties.get("Status")) or _property_text(properties.get("状态"))
    return status_value == "🔴已到期"


def build_google_calendar_event(page: dict[str, Any]) -> dict[str, Any] | None:
    """Google Calendar へそのまま投入できるイベント形式へ変換する。"""

    if not is_expired_project(page):
        return None

    properties = page.get("properties", {})
    title = (
        _property_text(properties.get("项目"))
        or _property_text(properties.get("Title"))
        or _property_text(properties.get("Name"))
        or "Untitled"
    )
    start_text = (
        _property_text(properties.get("维护预定日"))
        or _property_text(properties.get("DueDate"))
        or _property_text(properties.get("Date"))
        or _property_text(properties.get("TargetDate"))
        or _property_text(properties.get("StartDate"))
    )
    if not start_text:
        return None

    start_date = date.fromisoformat(start_text)
    end_date = start_date + timedelta(days=1)
    description = (
        _property_text(properties.get("备注"))
        or _property_text(properties.get("Summary"))
        or _property_text(properties.get("Description"))
        or f"Status: {_property_text(properties.get('Status')) or _property_text(properties.get('状态'))}"
    )

    return {
        "summary": title,
        "description": description,
        "location": None,
        "visibility": "public",
        "start": {"date": start_date.isoformat()},
        "end": {"date": end_date.isoformat()},
        "source": {"title": "Notion CL250", "url": page.get("url")},
    }


def build_apple_calendar_ics(events: list[dict[str, Any]]) -> str:
    """Apple Calendar へ貼り付け可能な ICS 形式を生成する。"""

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Alaye//CL250 expired project exporter//EN",
        "CALSCALE:GREGORIAN",
    ]

    for index, event in enumerate(events, start=1):
        title = event["summary"]
        start_value = event["start"]["date"]
        end_value = event["end"]["date"]
        description = event.get("description") or ""
        lines.extend(
            [
                "BEGIN:VEVENT",
                f"UID:{index}-{title}",
                f"DTSTAMP:{date.today().strftime('%Y%m%dT000000Z')}",
                f"DTSTART;VALUE=DATE:{start_value.replace('-', '')}",
                f"DTEND;VALUE=DATE:{end_value.replace('-', '')}",
                f"SUMMARY:{title}",
                f"DESCRIPTION:{description}",
                "END:VEVENT",
            ]
        )

    lines.append("END:VCALENDAR")
    return "\n".join(lines)
