from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable, List, Sequence, Set, Tuple

from .cards import Card, RANKS, create_deck


@dataclass
class RangeComboSet:
    combos: List[Tuple[Card, Card]]
    total_combos: int

    @property
    def frequency(self) -> float:
        if self.total_combos == 0:
            return 0.0
        return len(self.combos) / self.total_combos


def _combo_matches(c1: Card, c2: Card, rank_one: str, rank_two: str, suited: str | None) -> bool:
    ranks = {c1.rank, c2.rank}
    if ranks != {rank_one, rank_two}:
        return False
    if suited == "s":
        return c1.suit == c2.suit
    if suited == "o":
        return c1.suit != c2.suit
    return True


def _pair_combo_matches(c1: Card, c2: Card, pair_rank: str) -> bool:
    return c1.rank == c2.rank == pair_rank


def _hand_representation(token: str) -> tuple[str, str | None]:
    suited = None
    raw = token.strip().upper()
    if raw.endswith("S"):
        suited = "s"
        raw = raw[:-1]
    elif raw.endswith("O"):
        suited = "o"
        raw = raw[:-1]
    if len(raw) != 2:
        raise ValueError(f"Unrecognized hand token '{token}'")
    high, low = raw[0], raw[1]
    if high not in RANKS or low not in RANKS:
        raise ValueError(f"Unknown rank in token '{token}'")
    if high == low:
        suited = None
    return raw, suited


def _expand_plus_token(token: str) -> List[str]:
    cleaned = token.strip()
    if not cleaned.endswith("+"):
        return [cleaned.upper()]

    base = cleaned[:-1]
    suffix = ""
    if base.lower().endswith("s") or base.lower().endswith("o"):
        suffix = base[-1]
        base = base[:-1]

    if len(base) != 2:
        return [cleaned.upper()]

    first, second = base[0].upper(), base[1].upper()
    start_idx = RANKS.index(second)
    expanded: List[str] = []
    for rank in RANKS[start_idx:]:
        expanded.append(f"{first}{rank}{suffix}")
    return expanded


def parse_range_tokens(range_text: str) -> List[str]:
    cleaned = range_text.replace(" ", "")
    tokens: List[str] = []
    for raw_token in cleaned.split(","):
        if not raw_token:
            continue
        expanded = _expand_plus_token(raw_token)
        tokens.extend(token.upper() for token in expanded)
    return tokens or ["RANDOM"]


def _generate_combos_from_token(token: str, deck: Sequence[Card]) -> Set[Tuple[Card, Card]]:
    normalized = token.upper()
    if normalized in {"RANDOM", "ANY"}:
        return set(combinations(deck, 2))
    representation, suited = _hand_representation(normalized)
    if len(representation) != 2:
        return set()
    rank_one, rank_two = representation[0], representation[1]
    combos: Set[Tuple[Card, Card]] = set()
    for c1, c2 in combinations(deck, 2):
        ordered = tuple(sorted((c1, c2), key=lambda card: (card.value, card.suit)))
        if ordered in combos:
            continue
        if rank_one == rank_two:
            if _pair_combo_matches(*ordered, pair_rank=rank_one):
                combos.add(ordered)
        else:
            if _combo_matches(*ordered, rank_one, rank_two, suited):
                combos.add(ordered)
    return combos


def build_range(range_text: str, hero_cards: Iterable[Card] | None = None) -> RangeComboSet:
    hero_set = set(hero_cards or [])
    deck = create_deck(exclude=list(hero_set))
    tokens = parse_range_tokens(range_text)
    combos: Set[Tuple[Card, Card]] = set()
    for token in tokens:
        combos.update(_generate_combos_from_token(token, deck))
    total_available = len(list(combinations(deck, 2)))
    return RangeComboSet(sorted(combos, key=lambda pair: (pair[0].value, pair[0].suit, pair[1].value, pair[1].suit)), total_available)
