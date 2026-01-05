from __future__ import annotations

import argparse
from textwrap import dedent

from preflop_solver.cards import format_hand, parse_hand
from preflop_solver.simulation import estimate_equity
from preflop_solver.solver import PushFoldInputs, compute_push_ev


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Estimate preflop shove EV for heads-up scenarios using Monte Carlo simulation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=dedent(
            """
            Examples:
              python preflop_solver_cli.py --hero AhKs
              python preflop_solver_cli.py --hero QhJh --villain-range "77+,ATs+,KQo" --stack 20 --pot 1.5 --iterations 8000
            """
        ),
    )
    parser.add_argument("--hero", required=True, help="Hero hand, e.g. AhKd or 9c9d")
    parser.add_argument("--villain-range", default="random", help="Villain calling range such as '77+,ATs+,KQo'.")
    parser.add_argument("--stack", type=float, default=20.0, help="Effective stack in big blinds for the shove.")
    parser.add_argument("--pot", type=float, default=1.5, help="Current pot in big blinds (include blinds/antes).")
    parser.add_argument("--iterations", type=int, default=5000, help="Monte Carlo iterations (larger is slower but more accurate).")
    parser.add_argument("--seed", type=int, default=None, help="Optional RNG seed for reproducibility.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    hero_cards = parse_hand(args.hero)
    equity, villain_range = estimate_equity(hero_cards, args.villain_range, iterations=args.iterations, seed=args.seed)

    inputs = PushFoldInputs(stack_bb=args.stack, pot_bb=args.pot, equity=equity, villain_range=villain_range)
    result = compute_push_ev(inputs)

    print("Preflop shove EV estimate")
    print("========================\n")
    print(f"Hero: {format_hand(hero_cards)}")
    print(f"Villain calling range: {args.villain_range}")
    print(f"Equity vs calling range: {equity * 100:.2f}%")
    print(f"Villain calls: {result.call_frequency * 100:.2f}% of hands")
    print(f"Pot: {args.pot:.2f} bb | Stack risked: {args.stack:.2f} bb")
    print(f"EV(push): {result.ev_push:.3f} bb | EV(fold): {result.ev_fold:.3f} bb")
    print(f"Recommendation: {result.recommendation}")


if __name__ == "__main__":
    main()
