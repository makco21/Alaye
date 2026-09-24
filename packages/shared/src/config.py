"""アプリケーション設定を環境変数から読み込む。"""

from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()


class ConfigurationError(ValueError):
    """必須設定が不足している場合に送出する。"""


@dataclass(frozen=True)
class Settings:
    """外部サービス接続に必要な設定。"""

    notion_token: str
    notion_version: str = "2022-06-28"
    notion_records_database_id: str | None = None
    notion_tasks_database_id: str | None = None
    notion_projects_database_id: str | None = None
    notion_areas_database_id: str | None = None
    notion_cl250_database_id: str | None = None
    notion_maintenance_records_database_id: str | None = None
    notion_maintenance_projects_database_id: str | None = None
    notion_my_tasks_database_id: str | None = None
    notion_untitled_database_id: str | None = None
    notion_people_database_id: str | None = None
    notion_morning_database_id: str | None = None
    notion_keywords_database_id: str | None = None


def load_settings() -> Settings:
    """`.env` または環境変数を検証して設定を返す。"""

    notion_token = os.getenv("NOTION_TOKEN", "").strip()
    if not notion_token:
        raise ConfigurationError("NOTION_TOKEN is required")

    notion_version = os.getenv("NOTION_VERSION", "2022-06-28").strip()
    records_database_id = os.getenv("NOTION_RECORDS_DATABASE_ID", "").strip() or None
    tasks_database_id = os.getenv("NOTION_TASKS_DATABASE_ID", "").strip() or None
    projects_database_id = os.getenv("NOTION_PROJECTS_DATABASE_ID", "").strip() or None
    areas_database_id = os.getenv("NOTION_AREAS_DATABASE_ID", "").strip() or None
    cl250_database_id = os.getenv("NOTION_CL250_DATABASE_ID", "").strip() or None
    maintenance_records_database_id = (
        os.getenv("NOTION_MAINTENANCE_RECORDS_DATABASE_ID", "").strip() or None
    )
    maintenance_projects_database_id = (
        os.getenv("NOTION_MAINTENANCE_PROJECTS_DATABASE_ID", "").strip() or None
    )
    my_tasks_database_id = os.getenv("NOTION_MY_TASKS_DATABASE_ID", "").strip() or None
    untitled_database_id = os.getenv("NOTION_UNTITLED_DATABASE_ID", "").strip() or None
    people_database_id = os.getenv("NOTION_PEOPLE_DATABASE_ID", "").strip() or None
    morning_database_id = os.getenv("NOTION_MORNING_DATABASE_ID", "").strip() or None
    keywords_database_id = os.getenv("NOTION_KEYWORDS_DATABASE_ID", "").strip() or None
    return Settings(
        notion_token=notion_token,
        notion_version=notion_version,
        notion_records_database_id=records_database_id,
        notion_tasks_database_id=tasks_database_id,
        notion_projects_database_id=projects_database_id,
        notion_areas_database_id=areas_database_id,
        notion_cl250_database_id=cl250_database_id,
        notion_maintenance_records_database_id=maintenance_records_database_id,
        notion_maintenance_projects_database_id=maintenance_projects_database_id,
        notion_my_tasks_database_id=my_tasks_database_id,
        notion_untitled_database_id=untitled_database_id,
        notion_people_database_id=people_database_id,
        notion_morning_database_id=morning_database_id,
        notion_keywords_database_id=keywords_database_id,
    )