"""Notion の Records データベースを読み取る CLI。"""

import argparse

from packages.application.src.records import list_records


def main() -> None:
    """Records の内容を安全に表示する。"""

    parser = argparse.ArgumentParser()
    parser.add_argument("--view", default="all", help="Records View name")
    arguments = parser.parse_args()

    records = list_records(view_name=arguments.view)
    print(f"Records fetched: {len(records)}")
    for record in records:
        print(f"- {record.title} ({record.id})")
        if record.recorded_at:
            print(f"  Recorded at: {record.recorded_at}")
        if record.url:
            print(f"  URL: {record.url}")


if __name__ == "__main__":
    main()