# Santa 2026 Solver — Architecture Design

**Owner:** S Haider (`shaideroff`)  
**Participation:** Solo  
**Strategy:** Hybrid research and independent implementation

## Design goals
- Minimise the official competition objective: total instruction count across all scored puzzles.
- Generate only programs accepted by the official virtual-machine semantics and evaluator.
- Support multiple independently developed candidate generators.
- Make experiments reproducible and per-puzzle regressions inspectable.
- Run initially on free local/Kaggle CPU infrastructure; use acceleration only when benchmarks justify it.

## Source of truth and assumptions
The official competition overview, rules, input files, sample submission, and evaluator are authoritative. Previously discussed numeric limits must be rechecked against live official materials before they are encoded as constants. Unofficial notebook scores are not verified leaderboard results.

## Components
1. **Competition adapter:** reads official data and writes the exact required submission schema; contains no search logic.
2. **Machine model:** defines instruction representation, operand encoding, register state, operation semantics, and execution. Legality uses exact integer arithmetic and the official division rule.
3. **Candidate solver interface:** each engine accepts an immutable puzzle specification and configuration, and returns a candidate plus diagnostics.
4. **Constructive solver:** creates a deterministic legal baseline using mathematical decomposition and reusable intermediates.
5. **Search engines:** separate bounded search implementations such as beam search and target-directed/backward search.
6. **DAG optimiser:** identifies reusable expressions and lowers them into calculator instructions.
7. **Register allocator:** maps live DAG values to physical registers while respecting the official overwrite and operand rules.
8. **Portfolio selector:** validates candidates and selects the lowest-cost valid candidate; keeps a valid constructive fallback.
9. **Independent validator:** checks syntax, operands, exact arithmetic, machine constraints, limits, and target coverage.
10. **Benchmark harness:** records commit, configuration, seed, runtime, memory where available, per-puzzle counts, invalid count, and aggregate objective.

## Data flow
Official data -> adapter -> puzzle specifications -> candidate engines -> candidate pool -> validator -> portfolio selector -> validator again -> submission builder -> schema/size checks -> submission artifact.

## Failure handling
- A solver timeout or exception is recorded against that engine and puzzle; other engines continue.
- An invalid candidate is rejected with a structured reason.
- If a puzzle has no valid candidate, the run is incomplete and submission generation fails closed.
- Missing or malformed inputs stop the run before search.
- A malformed or partially written submission is never treated as successful output.

## Testing
- Unit tests for arithmetic operations and instruction encoding.
- Differential tests against official evaluator semantics when available.
- Boundary tests for register bounds, instruction limits, exact division, overwrite order, and output size.
- Property tests for interpreter consistency and expression lowering.
- Solver tests on small hand-constructed puzzles.
- End-to-end test from official input fixture to validated submission.
- Regression tests for every discovered failure and best-known benchmark corpus.

## Research and attribution
Study public notebooks and papers as ideas; independently reimplement algorithms, preserve licences and attribution, and record source URLs. Do not copy code with incompatible licence terms.

## Security and project boundaries
Owned by the personal `shaideroff` account. Kaggle tokens, private datasets, credentials, and account cookies must never be committed. No AWS resources, paid APIs, or Spunky Tech company infrastructure are required initially.

## Open implementation decisions
- Resolve exact instruction set, data schema, score definition, and hard limits from official competition materials before coding.
- Start in Python; introduce C++ only after profiling identifies a measurable bottleneck.
- Determine search budgets and concurrency empirically from free-tier runtime and memory constraints.
- Keep private during competitive development unless the owner explicitly chooses otherwise.