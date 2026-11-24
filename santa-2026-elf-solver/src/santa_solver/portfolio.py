"""Verified per-puzzle portfolio selection across independent submissions."""
from __future__ import annotations

from pathlib import Path
from typing import Sequence

from .model import Puzzle, read_submission, validate_program


def merge_portfolios(
    puzzles: Sequence[Puzzle], sources: Sequence[str | Path]
) -> tuple[dict[str, list[list]], dict[str, int]]:
    """Choose the shortest independently valid candidate for every puzzle.

    Source order is the deterministic tie-breaker. Invalid individual programs
    are counted and skipped; a puzzle with no valid candidate fails closed.
    Every candidate is replayed against the exact puzzle before selection.
    """
    if not sources:
        raise ValueError("at least one source submission is required")
    best: dict[str, list[list]] = {}
    best_cost: dict[str, int] = {}
    invalid = 0
    available = 0
    known = {p.id: p for p in puzzles}
    for source in sources:
        path = Path(source)
        programs = read_submission(path)
        extra = set(programs) - set(known)
        if extra:
            raise ValueError(f"{path}: contains {len(extra)} unknown puzzle IDs")
        for puzzle_id, program in programs.items():
            available += 1
            try:
                result = validate_program(known[puzzle_id], program)
            except ValueError:
                invalid += 1
                continue
            cost = result.instructions
            if puzzle_id not in best_cost or cost < best_cost[puzzle_id]:
                best[puzzle_id] = program
                best_cost[puzzle_id] = cost
    missing = set(known) - set(best)
    if missing:
        raise ValueError(f"no valid candidate for {len(missing)} puzzle(s): {sorted(missing)[:5]}")
    baseline = read_submission(sources[0])
    baseline_cost = {}
    for puzzle_id, program in baseline.items():
        if puzzle_id in known:
            try:
                baseline_cost[puzzle_id] = validate_program(known[puzzle_id], program).instructions
            except ValueError:
                pass
    report = {
        "source_files": len(sources),
        "candidate_programs": available,
        "invalid_candidates": invalid,
        "puzzles": len(puzzles),
        "total_instructions": sum(best_cost.values()),
        "puzzles_improved": sum(
            puzzle_id in baseline_cost and best_cost[puzzle_id] < baseline_cost[puzzle_id]
            for puzzle_id in known
        ),
    }
    return best, report
