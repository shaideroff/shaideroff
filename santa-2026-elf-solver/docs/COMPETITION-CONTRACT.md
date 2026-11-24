# Official competition contract (verified 2026-11-24)

- 1,000 scored puzzles and 200 practice puzzles.
- Score is the sum of instruction counts across the 1,000 scored puzzles; lower is better.
- 48 registers indexed 0–47; initial values occupy the first registers.
- Instruction `[op, i, j, d]` uses `+`, `-`, `*`, `/`; both sources are read before destination overwrite.
- Every result must be a positive integer, no greater than puzzle `value_limit` (maximum 10^18).
- Subtraction must be positive; division exact; source registers must be defined.
- A target is covered on first occurrence, even when its register is overwritten later.
- Every instruction counts; <=4,096 instructions and <=131,072 UTF-8 bytes per program.
- UTF-8 CSV header exactly `id,program`; each scored ID exactly once; program is a JSON instruction array.
- Any invalid program rejects the entire submission; no partial credit.
- Data download requires sign-in and explicit rules acceptance.

The validator's internal execution environment (hardware, memory, runtime and tie-breaking) was not disclosed in the official evaluation text reviewed and is intentionally not assumed.