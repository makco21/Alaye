"""Google Calendar API の薄いクライアント。"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def append_google_calendar_events(
	events: list[dict[str, Any]],
	credentials_path: str | Path,
	token_path: str | Path,
	calendar_id: str = "primary",
) -> list[dict[str, Any]]:
	"""通过 OAuth 将事件追加到 Google Calendar，并返回已创建事件。"""

	try:
		from google.auth.transport.requests import Request
		from google.oauth2.credentials import Credentials
		from google_auth_oauthlib.flow import InstalledAppFlow
		from googleapiclient.discovery import build
	except ImportError as error:
		raise RuntimeError(
			"Google Calendar dependencies are required; install requirements.txt"
		) from error

	scopes = ["https://www.googleapis.com/auth/calendar.events"]
	credentials_file = Path(credentials_path)
	token_file = Path(token_path)
	credentials = None
	if token_file.exists():
		credentials = Credentials.from_authorized_user_file(str(token_file), scopes)
	if not credentials or not credentials.valid:
		if credentials and credentials.expired and credentials.refresh_token:
			credentials.refresh(Request())
		else:
			if not credentials_file.exists():
				raise FileNotFoundError(f"Google OAuth credentials not found: {credentials_file}")
			credentials = InstalledAppFlow.from_client_secrets_file(
				str(credentials_file), scopes
			).run_local_server(port=0)
		token_file.write_text(credentials.to_json(), encoding="utf-8")

	service = build("calendar", "v3", credentials=credentials)
	created_events = []
	for event in events:
		body = {
			key: event[key]
			for key in ("summary", "description", "location", "visibility", "start", "end")
			if key in event and event[key] is not None
		}
		created_events.append(
			service.events().insert(calendarId=calendar_id, body=body).execute()
		)
	return created_events
