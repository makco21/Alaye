"""CL250 の期限切れプロジェクトを日历向け形式へ変換する CLI。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from packages.integrations.calendar.src.mapper import (
    build_apple_calendar_ics,
    build_google_calendar_event,
    is_expired_project,
)
from packages.integrations.calendar.src.client import append_google_calendar_events
from packages.integrations.notion.src.client import query_database
from packages.shared.src.config import ConfigurationError, load_settings


def list_expired_cl250_projects() -> list[dict]:
    """CL250 の expired ステータスのページだけを取得する。"""

    settings = load_settings()
    database_id = settings.notion_cl250_database_id
    if not database_id:
        raise ConfigurationError("NOTION_CL250_DATABASE_ID is required")

    pages = query_database(database_id)
    return [page for page in pages if is_expired_project(page)]


def main() -> None:
    """CL250 の expired 項目を Google Calendar / Apple Calendar 向け形式へ出力する。"""

    parser = argparse.ArgumentParser(description="Export expired CL250 projects as calendar events")
    parser.add_argument(
        "--format",
        choices=["google", "apple", "json"],
        default="google",
        help="Output format for calendar import",
    )
    parser.add_argument(
        "--append-to-google",
        action="store_true",
        help="Append Google-format events to Google Calendar",
    )
    parser.add_argument(
        "--calendar-id",
        default="primary",
        help="Google Calendar ID (default: primary)",
    )
    parser.add_argument(
        "--google-credentials",
        type=Path,
        default=Path("credentials.json"),
        help="Google OAuth client secrets JSON path",
    )
    parser.add_argument(
        "--google-token",
        type=Path,
        default=Path("token.json"),
        help="Google OAuth token JSON path",
    )
    args = parser.parse_args()

    pages = list_expired_cl250_projects()
    events = [
        event
        for page in pages
        if (event := build_google_calendar_event(page)) is not None
    ]

    if args.format == "json":
        print(json.dumps(events, ensure_ascii=False, indent=2))
        return

    if args.format == "google" and args.append_to_google:
        created_events = append_google_calendar_events(
            events,
            credentials_path=args.google_credentials,
            token_path=args.google_token,
            calendar_id=args.calendar_id,
        )
        print(f"Appended {len(created_events)} event(s) to Google Calendar {args.calendar_id}")
        return

    if args.format == "apple":
        print(build_apple_calendar_ics(events))
        return

    print(json.dumps(events, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
