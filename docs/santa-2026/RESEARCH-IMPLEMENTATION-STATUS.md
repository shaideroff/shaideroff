# Santa 2026 — Research and implementation status

Research completed: 2026-11-24 using official Kaggle pages, Parallel research, and direct GitHub repository inspection.

## Official competition contract
- 1,000 scored puzzles; score is sum of all instruction counts, lower is better.
- One invalid program rejects the complete submission.
- Machine: 48 registers, positive integer values, four arithmetic operators, exact division, subtraction strictly positive, no intermediate above per-puzzle value_limit.
- Every target needs to occur at least once; target remains covered after overwrite.
- Maximum 4,096 instructions and 131,072 UTF-8 bytes per program.
- CSV header exactly `id,program`; each scored puzzle ID exactly once.
- Official data page has 1,000 scored puzzles, 200 practice puzzles and the sample submission. Rule acceptance and login are required to download data.

## Research references
- Juan-Severiano/santa-2026: https://github.com/Juan-Severiano/santa-2026 — deterministic radix and signed-window constructors, independent replay validator, portfolio fallback, extensive search/rewrite work. README claims accepted Kaggle checkpoint 132,515 on 2026-11-21 (submission 58675401). Provenance and Apache-2.0 upstream notices are documented in THIRD_PARTY.md; do not blindly copy code.
- robsartin/elf-abacus: https://github.com/robsartin/elf-abacus — Apache-2.0; verifier-first architecture, Python plus optional native C kernel.
- Hansen0223/Santa_2026: https://github.com/Hansen0223/Santa_2026 — reported local portfolio 138,845; its README explicitly separates inherited public programs; no Kaggle receipt was verified.
- Joe-You-Know/PRTA-Elf-Calculator: https://github.com/Joe-You-Know/PRTA-Elf-Calculator — Apache-2.0; exact validator plus experimental graph rewrite research.
- Kaggle notebook Aman Atar: https://www.kaggle.com/code/amanatar/santa-2026-fast-validator-eda-sota-baseline/notebook — public score 142,909 on observed version 12, Apache 2.0.

## S Haider implementation begun
- Independent exact-integer machine model and validator added in local project.
- Strict CSV reader/writer and exact ID coverage checks added.
- Eleven focused tests pass under installed pytest in this workspace.
- Dataset download, sample baseline replay, independent constructive solver, search engines and complete submission still pending.

## Environment limitation
The local workspace has no network access; pip could not retrieve build dependencies. Direct Python test execution succeeded using the preinstalled pytest. The connected GitHub actions cannot create repositories, so a dedicated private repo could not be created through this connector. Issue #2 tracks that bootstrap blocker. No Kaggle credentials or data were accessed.