from __future__ import annotations

import random
from itertools import combinations
from typing import Iterable, List, Sequence, Tuple

from .cards import Card, create_deck
from .evaluator import compare_hands
from .range_parser import RangeComboSet, build_range

SimulationResult = Tuple[int, int, int]


def _sample_board(deck: List[Card], exclude: Sequence[Card]) -> List[Card]:
    available = [card for card in deck if card not in exclude]
    return random.sample(available, 5)


def estimate_equity(
    hero_hand: Sequence[Card],
    villain_range_text: str,
    iterations: int = 5000,
    seed: int | None = None,
) -> tuple[float, RangeComboSet]:
    rng = random.Random(seed)
    hero_list = list(hero_hand)
    deck = create_deck(exclude=hero_list)
    villain_range = build_range(villain_range_text, hero_cards=hero_list)
    if not villain_range.combos:
        villain_range = build_range("random", hero_cards=hero_list)
    wins = ties = losses = 0

    villain_combos = villain_range.combos
    for _ in range(iterations):
        villain_hand = list(rng.choice(villain_combos))
        remaining = [card for card in deck if card not in villain_hand]
        board = rng.sample(remaining, 5)
        result = compare_hands(hero_list, villain_hand, board)
        if result > 0:
            wins += 1
        elif result < 0:
            losses += 1
        else:
            ties += 1
    total = wins + ties + losses
    equity = (wins + 0.5 * ties) / total if total else 0.0
    return equity, villain_range


def villain_call_frequency(villain_range: RangeComboSet) -> float:
    return villain_range.frequency
