import csv
import json
from pathlib import Path

from santa_solver.model import Puzzle
from santa_solver.portfolio import merge_portfolios


def _write(path: Path, rows):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["id", "program"])
        for puzzle_id, program in rows:
            writer.writerow([puzzle_id, json.dumps(program, separators=(",", ":"))])


def test_merge_chooses_shortest_valid_program_per_puzzle(tmp_path):
    puzzles = [Puzzle("a", (3,), (6,), 20), Puzzle("b", (4,), (8,), 20)]
    fallback = tmp_path / "fallback.csv"
    better = tmp_path / "better.csv"
    _write(fallback, [
        ("a", [["+", 0, 0, 1], ["+", 1, 0, 2]]),
        ("b", [["+", 0, 0, 1]]),
    ])
    _write(better, [("a", [["+", 0, 0, 1]])])
    programs, report = merge_portfolios(puzzles, [fallback, better])
    assert len(programs["a"]) == 1
    assert len(programs["b"]) == 1
    assert report["total_instructions"] == 2
    assert report["puzzles_improved"] == 1


def test_merge_ignores_invalid_candidate_and_keeps_fallback(tmp_path):
    puzzles = [Puzzle("a", (3,), (6,), 20)]
    fallback = tmp_path / "fallback.csv"
    invalid = tmp_path / "invalid.csv"
    _write(fallback, [("a", [["+", 0, 0, 1]])])
    _write(invalid, [("a", [["/", 0, 0, 1]])])
    programs, report = merge_portfolios(puzzles, [fallback, invalid])
    assert programs["a"] == [["+", 0, 0, 1]]
    assert report["invalid_candidates"] == 1


def test_merge_requires_each_puzzle_to_have_a_valid_candidate(tmp_path):
    puzzles = [Puzzle("a", (3,), (6,), 20)]
    source = tmp_path / "empty.csv"
    _write(source, [])
    try:
        merge_portfolios(puzzles, [source])
    except ValueError as exc:
        assert "no valid candidate" in str(exc)
    else:
        raise AssertionError("expected missing candidate failure")
