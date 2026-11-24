# Santa 2026 — The Elf Calculator

**Owner:** S Haider (`shaideroff`)
**Participation:** Individual
**Approach:** Hybrid research and independent implementation
**Ambition:** Competitive leaderboard performance
**Status:** Research and design

## Objective

Develop a reproducible solver portfolio for the Kaggle Santa 2026 — The Elf Calculator competition. Optimise total instruction count while producing only programs accepted by the official calculator semantics and submission validator.

## Engineering principles

- Treat the official competition rules, files, and evaluator as authoritative.
- Preserve exact integer arithmetic; never use floating-point approximations for legality decisions.
- Build independent candidate solvers and compare them under one evaluator.
- Optimise for the actual scored objective, not proxy metrics.
- Independently validate every generated program before submission.
- Record code revision, configuration, seed, runtime, puzzle coverage, and total instruction count for every experiment.
- Keep competition data, credentials, Kaggle tokens, and submissions containing private information out of Git history.

## Proposed architecture

1. **Competition adapter:** load the official data format and isolate Kaggle-specific I/O.
2. **Machine model:** implement exact instruction semantics and a reference interpreter.
3. **Constructive solver:** produce legal baseline programs using mathematical decompositions and reusable intermediate values.
4. **Search solvers:** experiment with bounded beam search and backward/target-directed search.
5. **DAG optimiser:** represent shared intermediate expressions and lower them to the register machine.
6. **Register allocator:** schedule temporary values within the official register constraints.
7. **Portfolio selector:** compare valid candidates per puzzle using the official instruction-count objective.
8. **Independent validator:** verify syntax, operand ranges, exact division, register constraints, limits, and target coverage.
9. **Submission builder:** emit the exact official submission schema and run end-to-end checks.

## Research workflow

- Read the current competition overview, rules, data description, and evaluation implementation.
- Record baseline score and local runtime before optimisation.
- Reproduce public solver ideas independently and cite their source in research notes.
- Run one controlled algorithm change per experiment.
- Keep a per-puzzle score vector to identify regressions and opportunities.
- Never claim leaderboard rank or score without a timestamped Kaggle result.

## Definition of done

- Local interpreter matches official semantics on supplied examples.
- All official training/example cases pass.
- Every scored puzzle receives a candidate program.
- Independent validation passes for every puzzle.
- Submission schema and file-size/instruction limits are satisfied.
- Results are reproducible from a documented commit and configuration.

## Scope boundary

This is an independent personal research project under `shaideroff`. It is not owned by or deployed through Spunky Tech. No cloud resources or paid APIs are required for the initial implementation.
