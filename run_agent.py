"""Small runner for the job agent."""
from __future__ import annotations

import argparse

from job_agent.agent import run as run_agent


def main() -> int:
    p = argparse.ArgumentParser(description="Run the day-to-day job checking agent")
    p.add_argument("--tasks", default="tasks.json", help="Path to tasks.json")
    args = p.parse_args()
    return run_agent(args.tasks)


if __name__ == "__main__":
    raise SystemExit(main())
