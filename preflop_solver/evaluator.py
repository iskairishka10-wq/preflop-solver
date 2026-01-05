from __future__ import annotations

from collections import Counter
from itertools import combinations
from typing import Iterable, List, Sequence, Tuple

from .cards import Card

HandRank = Tuple[int, List[int]]
CATEGORY_NAMES = [
    "high card",
    "pair",
    "two pair",
    "three of a kind",
    "straight",
    "flush",
    "full house",
    "four of a kind",
    "straight flush",
]


def _is_straight(values: List[int]) -> int | None:
    unique_values = sorted(set(values))
    if 14 in unique_values:
        unique_values.insert(0, 1)  # wheel support
    longest_high = None
    for i in range(len(unique_values) - 4):
        window = unique_values[i : i + 5]
        if window[4] - window[0] == 4 and len(set(window)) == 5:
            longest_high = window[-1]
    return longest_high


def _rank_five_cards(cards: Sequence[Card]) -> HandRank:
    values = [card.value for card in cards]
    suits = [card.suit for card in cards]
    value_counter = Counter(values)
    counts = sorted(value_counter.items(), key=lambda item: (-item[1], -item[0]))
    is_flush = max(Counter(suits).values()) == 5
    straight_high = _is_straight(values)

    if is_flush:
        flush_cards = sorted(cards, key=lambda card: card.value, reverse=True)
        flush_values = [card.value for card in flush_cards]
        flush_straight_high = _is_straight(flush_values)
        if flush_straight_high:
            return 8, [flush_straight_high]
        return 5, flush_values

    if counts[0][1] == 4:
        quad_value = counts[0][0]
        kicker = max(v for v in values if v != quad_value)
        return 7, [quad_value, kicker]

    if counts[0][1] == 3 and counts[1][1] >= 2:
        trips_value = counts[0][0]
        pair_value = counts[1][0]
        return 6, [trips_value, pair_value]

    if straight_high:
        return 4, [straight_high]

    if counts[0][1] == 3:
        trips_value = counts[0][0]
        kickers = [value for value, count in counts[1:] if count == 1][:2]
        return 3, [trips_value] + kickers

    if counts[0][1] == 2 and counts[1][1] == 2:
        high_pair, low_pair = counts[0][0], counts[1][0]
        kicker = max(v for v in values if v not in {high_pair, low_pair})
        return 2, [high_pair, low_pair, kicker]

    if counts[0][1] == 2:
        pair_value = counts[0][0]
        kickers = [value for value, count in counts[1:] if count == 1][:3]
        return 1, [pair_value] + kickers

    return 0, sorted(values, reverse=True)


def evaluate_seven(cards: Iterable[Card]) -> HandRank:
    best_rank: HandRank | None = None
    card_list = list(cards)
    if len(card_list) != 7:
        raise ValueError("Seven cards required for evaluation")
    for combo in combinations(card_list, 5):
        current_rank = _rank_five_cards(combo)
        if best_rank is None or current_rank > best_rank:
            best_rank = current_rank
    assert best_rank is not None
    return best_rank


def compare_hands(hero_cards: Sequence[Card], villain_cards: Sequence[Card], board: Sequence[Card]) -> int:
    hero_rank = evaluate_seven(list(hero_cards) + list(board))
    villain_rank = evaluate_seven(list(villain_cards) + list(board))
    if hero_rank > villain_rank:
        return 1
    if villain_rank > hero_rank:
        return -1
    return 0
