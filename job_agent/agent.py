"""Simple day-to-day job checking agent.

Reads a `tasks.json` file (workspace root) and produces a daily summary
report with counts of due, overdue, and completed tasks.
"""
from __future__ import annotations

import json
import os
from datetime import date
from typing import List, Dict, Any

from dateutil import parser as date_parser


def load_tasks(path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Tasks file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("tasks.json must be a list of task objects")
    return data


def _parse_date(val) -> date | None:
    if val is None:
        return None
    if isinstance(val, date):
        return val
    return date_parser.parse(val).date()


def due_today(tasks: List[Dict[str, Any]], today: date | None = None) -> List[Dict[str, Any]]:
    today = today or date.today()
    out = []
    for t in tasks:
        if t.get("status") == "done":
            continue
        d = _parse_date(t.get("due_date"))
        if d == today:
            out.append(t)
    return out


def overdue(tasks: List[Dict[str, Any]], today: date | None = None) -> List[Dict[str, Any]]:
    today = today or date.today()
    out = []
    for t in tasks:
        if t.get("status") == "done":
            continue
        d = _parse_date(t.get("due_date"))
        if d is not None and d < today:
            out.append(t)
    return out


def completed(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [t for t in tasks if t.get("status") == "done"]


def summary_report(tasks: List[Dict[str, Any]], today: date | None = None) -> Dict[str, Any]:
    today = today or date.today()
    due = due_today(tasks, today)
    over = overdue(tasks, today)
    done = completed(tasks)
    return {
        "date": today.isoformat(),
        "total_tasks": len(tasks),
        "due_today_count": len(due),
        "overdue_count": len(over),
        "completed_count": len(done),
        "due_today": due,
        "overdue": over,
        "completed": done,
    }


def write_report(report: Dict[str, Any], out_dir: str = "reports") -> str:
    os.makedirs(out_dir, exist_ok=True)
    filename = f"daily_{report['date']}.json"
    path = os.path.join(out_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    return path


def run(tasks_path: str = "tasks.json") -> int:
    try:
        tasks = load_tasks(tasks_path)
    except Exception as e:
        print(f"Error loading tasks: {e}")
        return 2
    report = summary_report(tasks)
    path = write_report(report)
    print(f"Daily report written: {path}")
    print(f"Total: {report['total_tasks']}  Due today: {report['due_today_count']}  Overdue: {report['overdue_count']}  Completed: {report['completed_count']}")
    if report["overdue_count"] > 0:
        print("Overdue items:")
        for t in report["overdue"]:
            print(f" - {t.get('title')} (due {t.get('due_date')})")
    return 0


if __name__ == "__main__":
    run()
