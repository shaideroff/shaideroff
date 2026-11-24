from pathlib import Path
import pytest
from santa_solver.model import Puzzle, read_submission, score_submission, validate_program, write_submission


def toy():
    return Puzzle("toy", (3,), (1, 2, 5, 8), 9, 48)


def test_official_toy_example():
    program = [["/", 0, 0, 1], ["-", 0, 1, 2], ["+", 0, 2, 3], ["+", 0, 3, 4]]
    result = validate_program(toy(), program)
    assert (result.instructions, result.covered_targets) == (4, 4)


def test_division_must_be_exact():
    with pytest.raises(ValueError, match="divides inexactly"):
        validate_program(Puzzle("div", (5, 2), (2,), 10), [["/", 0, 1, 2]])


def test_subtraction_result_must_be_positive():
    with pytest.raises(ValueError, match="value_limit"):
        validate_program(Puzzle("sub", (2, 2), (1,), 10), [["-", 0, 1, 2]])


def test_destination_can_overwrite_source_after_read():
    assert validate_program(Puzzle("overwrite", (3,), (6,), 10), [["+", 0, 0, 0]]).instructions == 1


def test_undefined_source_rejected():
    with pytest.raises(ValueError, match="undefined register"):
        validate_program(Puzzle("undef", (3,), (6,), 10), [["+", 0, 1, 2]])


def test_intermediate_limit_enforced():
    with pytest.raises(ValueError, match="value_limit"):
        validate_program(Puzzle("limit", (4, 4), (2,), 5), [["*", 0, 1, 2]])


def test_covered_target_remains_seen_after_overwrite():
    puzzle = Puzzle("covered", (3,), (6,), 10)
    program = [["+", 0, 0, 1], ["/", 0, 0, 1]]
    assert validate_program(puzzle, program).covered_targets == 1


def test_csv_json_round_trip(tmp_path: Path):
    puzzle = toy()
    program = [["/", 0, 0, 1], ["-", 0, 1, 2], ["+", 0, 2, 3], ["+", 0, 3, 4]]
    path = tmp_path / "submission.csv"
    write_submission(path, {puzzle.id: program})
    loaded = read_submission(path)
    assert loaded == {puzzle.id: program}
    assert score_submission([puzzle], loaded)[puzzle.id].instructions == 4


def test_exact_puzzle_ID_coverage():
    with pytest.raises(ValueError, match="ID mismatch"):
        score_submission([toy()], {})


def test_values_use_arbitrary_precision_ints():
    p = Puzzle("large", (10**18,), (10**18,), 10**18)
    assert validate_program(p, []).instructions == 0


def test_instruction_limit_enforced():
    p = Puzzle("cap", (1,), (), 10)
    with pytest.raises(ValueError, match="4096"):
        validate_program(p, [["+", 0, 0, 0]] * 4097)
