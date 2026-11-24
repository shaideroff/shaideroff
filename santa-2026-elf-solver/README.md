# Santa 2026 — The Elf Calculator

Independent solver engineering by **S Haider (`shaideroff`)**.

## Mission
Minimise the sum of calculator instructions across all 1,000 scored puzzles. Every program must be legal and produce every target at least once; a single invalid program rejects the whole submission.

## Official rules
- 48 registers, indexed 0–47; initial values occupy consecutive registers.
- Instruction format: `["op", source_i, source_j, destination]` with `+`, `-`, `*`, `/`.
- Both sources are read before destination overwrite.
- Results must be positive integers no greater than the puzzle's `value_limit` (at most 10^18).
- Subtraction must remain positive; division must be exact.
- All source registers must be defined.
- Targets count when seen, even if their register is later overwritten.
- Every instruction counts. Maximum 4,096 instructions and 131,072 UTF-8 bytes per program.
- Submission CSV has exactly `id,program`; all scored IDs exactly once; `program` is JSON.

Authoritative links: [Overview](https://www.kaggle.com/competitions/santa-2026/overview) · [Data](https://www.kaggle.com/competitions/santa-2026/data) · [Evaluation](https://www.kaggle.com/competitions/santa-2026/overview/evaluation) · [Rules](https://www.kaggle.com/competitions/santa-2026/rules)

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
pytest
```

Download official competition data only after login and accepting the rules:
```bash
kaggle competitions files santa-2026
kaggle competitions download santa-2026 -p data
```

Store data under `data/` (git-ignored). Do not publish competition data. Kaggle credentials never belong in source control.

## Local workflow

Validate a complete candidate submission:
```bash
santa-solver validate data/puzzles.csv data/candidate.csv
```

Merge several independently generated candidate portfolios. The first source is the fallback/tie-break baseline; every candidate is replayed against its puzzle and only the shortest valid program is retained:
```bash
santa-solver merge data/puzzles.csv outputs/merged.csv \
  data/baseline.csv data/public-frontier.csv data/experimental.csv
```

The merge command reopens and validates the serialized output. It does not submit to Kaggle. Keep competition data and generated submissions local and git-ignored.

## Status
- [x] Exact integer reference machine and validator
- [x] Strict CSV/JSON parsing and round-trip writer
- [x] Official 1,000-puzzle sample replay (1,490,379 instructions; zero invalid programs)
- [x] Deterministic per-puzzle portfolio merge with invalid-candidate rejection
- [ ] Competitive public/reference portfolio acquisition and provenance audit
- [ ] Constructive solver portfolio and search/graph optimisation
- [ ] Full 1,000-puzzle benchmark and final submission

No Kaggle submission is made automatically.
