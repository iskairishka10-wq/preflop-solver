from __future__ import annotations

from dataclasses import dataclass

from .range_parser import RangeComboSet


@dataclass
class PushFoldInputs:
    stack_bb: float
    pot_bb: float
    equity: float
    villain_range: RangeComboSet


@dataclass
class PushFoldResult:
    ev_push: float
    ev_fold: float
    call_frequency: float

    @property
    def recommendation(self) -> str:
        if self.ev_push > self.ev_fold:
            return "Push"
        if self.ev_push < self.ev_fold:
            return "Fold"
        return "Indifferent"


def compute_push_ev(inputs: PushFoldInputs) -> PushFoldResult:
    call_freq = inputs.villain_range.frequency
    fold_freq = 1 - call_freq

    pot_if_called = inputs.pot_bb + inputs.stack_bb
    win_if_called = inputs.equity * pot_if_called
    loss_if_called = (1 - inputs.equity) * inputs.stack_bb

    ev_push = fold_freq * inputs.pot_bb + call_freq * (win_if_called - loss_if_called)
    ev_fold = 0.0
    return PushFoldResult(ev_push=ev_push, ev_fold=ev_fold, call_frequency=call_freq)
