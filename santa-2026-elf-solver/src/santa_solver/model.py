"""Exact reference machine and submission schema for Santa 2026."""
from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

MAX_INSTRUCTIONS = 4096
MAX_PROGRAM_BYTES = 131072
MAX_REGISTERS = 48
MAX_VALUE = 10**18
OPERATORS = {"+", "-", "*", "/"}


def _positive_int(value: object, label: str, upper: int) -> None:
    if type(value) is not int or not 1 <= value <= upper:
        raise ValueError(f"{label} must be an integer in [1, {upper}]")


@dataclass(frozen=True)
class Puzzle:
    id: str
    starting_values: tuple[int, ...]
    targets: tuple[int, ...]
    value_limit: int
    registers: int = MAX_REGISTERS

    def __post_init__(self) -> None:
        if not isinstance(self.id, str) or not self.id:
            raise ValueError("puzzle id must be nonempty")
        _positive_int(self.value_limit, "value_limit", MAX_VALUE)
        _positive_int(self.registers, "registers", MAX_REGISTERS)
        if not self.starting_values or len(self.starting_values) > self.registers:
            raise ValueError("starting_values must be nonempty and fit the register bank")
        for value in self.starting_values:
            _positive_int(value, "starting value", self.value_limit)
        for value in self.targets:
            _positive_int(value, "target", self.value_limit)


@dataclass(frozen=True)
class ValidationResult:
    instructions: int
    covered_targets: int


def _json_text(program: object) -> str:
    try:
        return json.dumps(program, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("program is not JSON serializable") from exc


def validate_shape(program: object) -> list[list]:
    if type(program) is not list:
        raise ValueError("program must be a JSON array")
    if len(program) > MAX_INSTRUCTIONS:
        raise ValueError(f"program exceeds {MAX_INSTRUCTIONS} instructions")
    for n, inst in enumerate(program, 1):
        if type(inst) is not list or len(inst) != 4:
            raise ValueError(f"instruction {n} must be [op, left, right, destination]")
        op, left, right, dest = inst
        if type(op) is not str or op not in OPERATORS:
            raise ValueError(f"instruction {n} has an invalid operator")
        if any(type(i) is not int or not 0 <= i < MAX_REGISTERS for i in (left, right, dest)):
            raise ValueError(f"instruction {n} has an invalid register index")
    if len(_json_text(program).encode("utf-8")) > MAX_PROGRAM_BYTES:
        raise ValueError(f"program exceeds {MAX_PROGRAM_BYTES} UTF-8 bytes")
    return program


def validate_program(puzzle: Puzzle, program: object) -> ValidationResult:
    program = validate_shape(program)
    regs: list[int | None] = [None] * puzzle.registers
    regs[: len(puzzle.starting_values)] = puzzle.starting_values
    missing = set(puzzle.targets).difference(puzzle.starting_values)
    for n, (op, left, right, dest) in enumerate(program, 1):
        if max(left, right, dest) >= puzzle.registers:
            raise ValueError(f"{puzzle.id}: instruction {n} exceeds puzzle register count")
        a, b = regs[left], regs[right]
        if a is None or b is None:
            raise ValueError(f"{puzzle.id}: instruction {n} reads an undefined register")
        if op == "+":
            value = a + b
        elif op == "-":
            value = a - b
        elif op == "*":
            value = a * b
        else:
            value, rem = divmod(a, b)
            if rem:
                raise ValueError(f"{puzzle.id}: instruction {n} divides inexactly")
        if not 1 <= value <= puzzle.value_limit:
            raise ValueError(f"{puzzle.id}: instruction {n} produces a value outside value_limit")
        regs[dest] = value
        missing.discard(value)
    if missing:
        raise ValueError(f"{puzzle.id}: {len(missing)} target(s) were not produced")
    return ValidationResult(len(program), len(set(puzzle.targets)))


def read_puzzles(path: str | Path) -> list[Puzzle]:
    required = {"id", "starting_values", "targets", "value_limit", "registers"}
    out: list[Puzzle] = []
    seen: set[str] = set()
    with Path(path).open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, strict=True)
        if not reader.fieldnames or len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError("puzzles CSV has missing or duplicate column names")
        if not required.issubset(reader.fieldnames):
            raise ValueError(f"puzzles CSV missing columns: {sorted(required - set(reader.fieldnames))}")
        for rownum, row in enumerate(reader, 2):
            if None in row or any(v is None for v in row.values()):
                raise ValueError(f"puzzles CSV row {rownum} has an incorrect number of cells")
            try:
                start = json.loads(row["starting_values"])
                targets = json.loads(row["targets"])
                if type(start) is not list or type(targets) is not list:
                    raise ValueError("starting_values and targets must be JSON arrays")
                puzzle = Puzzle(row["id"], tuple(start), tuple(targets), int(row["value_limit"]), int(row["registers"]))
            except (json.JSONDecodeError, TypeError, ValueError) as exc:
                raise ValueError(f"invalid puzzle row {rownum}: {exc}") from exc
            if puzzle.id in seen:
                raise ValueError(f"duplicate puzzle ID: {puzzle.id}")
            seen.add(puzzle.id)
            out.append(puzzle)
    if not out:
        raise ValueError("puzzles CSV is empty")
    return out


def read_submission(path: str | Path) -> dict[str, list[list]]:
    out: dict[str, list[list]] = {}
    with Path(path).open("r", encoding="utf-8", newline="") as stream:
        reader = csv.reader(stream, strict=True)
        if next(reader, None) != ["id", "program"]:
            raise ValueError("submission CSV header must be exactly id,program")
        for rownum, row in enumerate(reader, 2):
            if len(row) != 2 or not row[0]:
                raise ValueError(f"submission row {rownum} must contain ID and program")
            if row[0] in out:
                raise ValueError(f"duplicate submission ID: {row[0]}")
            if len(row[1].encode("utf-8")) > MAX_PROGRAM_BYTES:
                raise ValueError(f"{row[0]}: program exceeds UTF-8 byte limit")
            try:
                out[row[0]] = validate_shape(json.loads(row[1]))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{row[0]}: invalid program JSON: {exc}") from exc
    return out


def write_submission(path: str | Path, programs: Mapping[str, list[list]]) -> None:
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for identifier, program in programs.items():
        if not isinstance(identifier, str) or not identifier:
            raise ValueError("submission ID must be a nonempty string")
        validate_shape(program)
        rows.append((identifier, _json_text(program)))
    with dest.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["id", "program"])
        writer.writerows(rows)


def score_submission(puzzles: Sequence[Puzzle], programs: Mapping[str, list[list]]) -> dict[str, ValidationResult]:
    expected = {p.id for p in puzzles}
    if len(expected) != len(puzzles):
        raise ValueError("duplicate puzzle IDs")
    if set(programs) != expected:
        raise ValueError(f"submission ID mismatch: {len(expected - set(programs))} missing, {len(set(programs) - expected)} extra")
    return {p.id: validate_program(p, programs[p.id]) for p in puzzles}
