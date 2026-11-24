# S Haider — Santa 2026 Development Plan

## Research-backed algorithm plan

1. **Reference layer:** exact Python integer interpreter, schema parser, validator, CSV/JSON round trip. This is the source of truth for every solver.
2. **Trusted baseline:** download and replay official `sample_submission.csv`; record hash, score, max program length and per-puzzle vector.
3. **Independent constructors:** positional radix portfolio; signed binary-window constructions; direct target closure; small exact constants and safe reuse.
4. **Multi-target search:** reachable-value dictionary, target-order variants, common factors/differences, bounded beam and backward meet-in-the-middle.
5. **DAG-level optimisation:** shared-expression extraction, local graph resynthesis, peephole replacement, target-event preservation.
6. **Register allocation:** liveness-aware physical assignment over 48 registers; verify register overwrites and semantics after lowering.
7. **Portfolio selection:** keep shortest valid program per puzzle and preserve best-known fallback. Never accept a candidate solely on estimated cost.
8. **Release gate:** validate every one of the 1,000 IDs, round-trip the actual CSV, validate again, check all size limits and archive hashes before manual submission.

## Open-source research

- `Juan-Severiano/santa-2026`: https://github.com/Juan-Severiano/santa-2026 — accepted 132,515 checkpoint reported in README; deterministic radix/window portfolio, Python exact validator and extensive repair work. README and THIRD_PARTY disclose upstream Apache-2.0 components. Provenance must travel with any derivative.
- `robsartin/elf-abacus`: https://github.com/robsartin/elf-abacus — Apache-2.0, verifier-first Python design and optional native C kernel.
- `Hansen0223/Santa_2026`: https://github.com/Hansen0223/Santa_2026 — local score claim 138,845; inherited public program contributions explicitly disclosed; no official receipt confirmed in inspected excerpt.
- `Joe-You-Know/PRTA-Elf-Calculator`: https://github.com/Joe-You-Know/PRTA-Elf-Calculator — Apache-2.0, validator and experimental graph rewrites; claimed new algebraic generator remains experimental.
- `Aman Atar notebook`: https://www.kaggle.com/code/amanatar/santa-2026-fast-validator-eda-sota-baseline/notebook — observed version 12 score 142,909 and Apache 2.0 licence.

Treat public Kaggle pages, programs and solver code as distinct licensing objects. Public visibility does not grant blanket code reuse. Verify licence and upstream attributions for each snapshot. Keep public-program portfolio scores separate from S Haider-authored algorithmic improvements.

## Execution constraints

CPU-first; no paid API/cloud requirement. Kaggle credentials and the rule-gated data stay out of Git. Use C++/Rust only after profiling identifies an actual hotspot. No automated submission; owner performs final Kaggle submission after validating output.