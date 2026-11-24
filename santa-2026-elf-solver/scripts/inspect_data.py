from __future__ import annotations
import argparse, json
from santa_solver.model import read_puzzles

p = argparse.ArgumentParser(description="Inspect official Santa puzzle CSV")
p.add_argument("csv")
a = p.parse_args()
puzzles = read_puzzles(a.csv)
print(json.dumps({"count":len(puzzles),"first_id":puzzles[0].id,"last_id":puzzles[-1].id,
                  "starting_values_min":min(len(x.starting_values) for x in puzzles),
                  "starting_values_max":max(len(x.starting_values) for x in puzzles),
                  "targets_min":min(len(x.targets) for x in puzzles),
                  "targets_max":max(len(x.targets) for x in puzzles),
                  "max_value_limit":max(x.value_limit for x in puzzles)},indent=2))
