from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence

RANKS = "23456789TJQKA"
SUITS = "cdhs"
RANK_TO_VALUE = {rank: index + 2 for index, rank in enumerate(RANKS)}
VALUE_TO_RANK = {value: rank for rank, value in RANK_TO_VALUE.items()}


@dataclass(frozen=True)
class Card:
    rank: str
    suit: str

    def __post_init__(self) -> None:
        if self.rank not in RANK_TO_VALUE:
            raise ValueError(f"Invalid rank: {self.rank}")
        if self.suit not in SUITS:
            raise ValueError(f"Invalid suit: {self.suit}")

    @property
    def value(self) -> int:
        return RANK_TO_VALUE[self.rank]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.rank}{self.suit}"


def create_deck(exclude: Sequence[Card] | None = None) -> List[Card]:
    excluded = set(exclude or [])
    return [card for card in (Card(rank, suit) for rank in RANKS for suit in SUITS) if card not in excluded]


def parse_card(token: str) -> Card:
    if len(token) != 2:
        raise ValueError(f"Card token must be two characters like Ah or Td, got '{token}'")
    rank, suit = token[0].upper(), token[1].lower()
    return Card(rank, suit)


def parse_hand(hand: str) -> List[Card]:
    cleaned = hand.replace(" ", "").replace("-", "")
    if len(cleaned) != 4:
        raise ValueError("Hand must contain exactly two cards, e.g. AhKd")
    return [parse_card(cleaned[:2]), parse_card(cleaned[2:])]


def format_hand(cards: Iterable[Card]) -> str:
    return " ".join(str(card) for card in cards)
