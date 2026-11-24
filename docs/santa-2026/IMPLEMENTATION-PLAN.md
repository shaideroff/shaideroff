# Santa 2026 Solver — Implementation Plan

**Owner:** S Haider (`shaideroff`)  
**Approach:** Hybrid  
**Execution:** Kaggle Notebook + GitHub, CPU-first

## Workstream 1 — Competition contract and machine model
**Proposed files:** `src/santa_solver/competition/adapter.py`, `src/santa_solver/core/instructions.py`, `src/santa_solver/core/machine.py`, `src/santa_solver/validation/validator.py`, `tests/test_machine.py`, `tests/test_validation.py`.

**Inputs:** official rules, sample input, sample submission, evaluator where available. **Outputs:** typed puzzle model, exact instruction representation, reference interpreter, structured validation report.

Tasks: record the official contract and source URLs; parse inputs without altering identifiers or target ordering; implement each instruction in a reference interpreter; implement state transitions and overwrite semantics; validate syntax and complete target coverage.

**Tests:** one case per operation; exact and inexact division; invalid register references; overwrites; empty and boundary programs; official samples; differential comparison to the official evaluator when possible.

**Acceptance:** the interpreter agrees with authoritative semantics and all official fixtures pass. No optimisation work before this gate is green.

## Workstream 2 — Constructive baseline and reproducible benchmark
**Proposed files:** `src/santa_solver/solvers/base.py`, `src/santa_solver/solvers/constructive.py`, `src/santa_solver/benchmarks/evaluator.py`, `configs/default.yaml`, `tests/test_constructive.py`.

**Inputs:** validated puzzle specifications. **Outputs:** legal baseline candidates, per-puzzle instruction counts, runtime and aggregate score report.

Tasks: define a common solver interface; implement a deterministic constructive baseline; run across the full official scored set; persist machine-readable results and a baseline score vector.

**Tests:** deterministic output for fixed config; constructive examples; unsupported cases reported as unsolved rather than emitting illegal instructions; full fixture coverage.

**Acceptance:** reproducible run, explicit unsolved count, no invalid output, baseline metrics recorded.

## Workstream 3 — Search and shared-expression optimisation
**Proposed files:** `src/santa_solver/solvers/beam_search.py`, `src/santa_solver/solvers/backward_search.py`, `src/santa_solver/optimization/dag.py`, `src/santa_solver/optimization/register_allocator.py`, `src/santa_solver/solvers/portfolio.py`, and focused tests.

**Inputs:** puzzle, validated baseline, compute budget. **Outputs:** candidate programs per puzzle.

Tasks: implement a configurable deterministic beam search; add a separate target-directed search engine; represent expressions as a DAG and identify common subexpressions; lower DAG operations into instructions and allocate registers through liveness analysis; select only independently valid candidates while preserving the baseline fallback.

**Tests:** small known constructions; search budget termination; deterministic seeds; DAG sharing on controlled cases; register liveness/reuse; invalid candidate rejection; baseline fallback.

**Acceptance:** every returned candidate passes independent validation and the benchmark shows a real aggregate objective improvement.

## Workstream 4 — Submission and release verification
**Proposed files:** `src/santa_solver/validation/submission.py`, `scripts/run_benchmark.py`, `scripts/build_submission.py`, `tests/test_submission.py`, CI workflow.

**Inputs:** selected candidates for every scored puzzle and the official schema/limits. **Outputs:** exact submission artifact and reproducibility manifest.

Tasks: serialize the official schema; re-read and independently validate every row; check completeness, uniqueness, size and per-program limits; record source commit, config, run time and score metrics; test from a clean environment.

**Tests:** schema round-trip; missing/duplicate puzzle; invalid program; size boundary; deterministic serialization; full scored fixture (expected puzzle count taken from official data).

**Acceptance:** zero invalid programs; official evaluator accepts the artifact; build is reproducible.

## Execution order
Workstream 1 -> Workstream 2 -> Workstream 3 -> Workstream 4. Search must not be tuned against an unverified machine model. C++ acceleration is conditional on profiling.

## Decisions to resolve from official materials
- Exact schema, semantics, score aggregation, numeric limits and instruction cap.
- Public release timing; default private during competition.
- C++ acceleration only if profiling demonstrates a bottleneck.