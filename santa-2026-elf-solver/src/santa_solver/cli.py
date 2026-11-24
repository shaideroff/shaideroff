"""Local inspection and validation commands. Never submits to Kaggle."""
from __future__ import annotations
import argparse
import csv
import json
import sys
from pathlib import Path
from .model import read_puzzles, read_submission, score_submission

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    inspect = sub.add_parser("inspect", help="Summarize an official puzzle CSV")
    inspect.add_argument("puzzles", type=Path)
    validate = sub.add_parser("validate", help="Independently replay every submission program")
    validate.add_argument("puzzles", type=Path)
    validate.add_argument("submission", type=Path)
    args = parser.parse_args(argv)
    try:
        puzzles = read_puzzles(args.puzzles)
        if args.command == "inspect":
            summary = {"count":len(puzzles),"first_id":puzzles[0].id,"last_id":puzzles[-1].id,
              "starting_values_min":min(len(p.starting_values) for p in puzzles),
              "starting_values_max":max(len(p.starting_values) for p in puzzles),
              "targets_min":min(len(p.targets) for p in puzzles),"targets_max":max(len(p.targets) for p in puzzles),
              "max_value_limit":max(p.value_limit for p in puzzles)}
        else:
            results = score_submission(puzzles, read_submission(args.submission))
            counts = [r.instructions for r in results.values()]
            summary = {"puzzles":len(counts),"total_instructions":sum(counts),
              "max_instructions":max(counts,default=0),"invalid_programs":0}
        print(json.dumps(summary, indent=2))
        return 0
    except (OSError, ValueError, csv.Error) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
