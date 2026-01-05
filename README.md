# preflop-solver

A lightweight heads-up preflop shove solver that estimates expected value (EV) using Monte Carlo simulations. Provide your hole cards, a villain calling range, stack size, and pot size to get a push/fold recommendation.

## Features

- Card/range parser that understands shorthand such as `77+`, `ATs+`, `KQo`, or `random`.
- Monte Carlo equity estimator versus a specified calling range.
- Push/fold EV calculation for heads-up scenarios with customizable stack and pot sizes.
- Command-line interface for quick what-if analysis.

## Usage

Run the CLI with Python (3.10+ recommended):

```bash
python preflop_solver_cli.py --hero AhKd --villain-range "77+,ATs+,KQo" --stack 20 --pot 1.5 --iterations 8000
```

Arguments:

- `--hero` (required): Hero hand, e.g. `AhKd` or `9c9d`.
- `--villain-range`: Villain calling range (default `random`). Supports `+` expansions like `77+` or `ATs+`.
- `--stack`: Effective stack in big blinds being shoved (default `20`).
- `--pot`: Current pot in big blinds including blinds/antes (default `1.5`).
- `--iterations`: Number of Monte Carlo samples (default `5000`).
- `--seed`: Optional RNG seed for reproducible outputs.

Example output:

```
Preflop shove EV estimate
========================

Hero: Ah Kd
Villain calling range: 77+,ATs+,KQo
Equity vs calling range: 59.20%
Villain calls: 9.68% of hands
Pot: 1.50 bb | Stack risked: 20.00 bb
EV(push): 1.242 bb | EV(fold): 0.000 bb
Recommendation: Push
```

## Notes

- Ranges are treated as villain **calling** ranges. Hands outside the specified range are assumed to fold.
- If the supplied range is empty or invalid, it falls back to `random`.
- The solver models heads-up all-in scenarios; adjust `pot` and `stack` to match your situation.
