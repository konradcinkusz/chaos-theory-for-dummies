import importlib.util
import random
from pathlib import Path

import pytest

from labs._loader import load

CH14 = Path(__file__).resolve().parents[2] / "ch14"


def _chapter(name: str):
    """Import one of the chapter's listings under a private name."""
    spec = importlib.util.spec_from_file_location(
        f"ch14_{name}", CH14 / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_chance_counts_the_members_that_rain() -> None:
    lab = load("ch14", "l14_01_chance")
    members = [(6.0, 0.0), (4.0, 9.0), (5.5, 1.0), (5.0, 2.0)]
    assert lab.chance(members, 5.0) == 0.5      # 5.0 itself is dry
    assert lab.chance(members, 5.0, site=1) == 0.25


def test_the_chapters_forecast_says_seventy_five_per_cent() -> None:
    lab = load("ch14", "l14_01_chance")
    ens = _chapter("ensemble")
    _, members = ens.ensemble(ens.spin_up(), random.Random(14))
    members = [ens.run(m, 70) for m in members]     # a lead of 3.5
    assert lab.chance(members, 5.0) == 0.75


def test_hit_rate_keeps_only_the_forecasts_in_range() -> None:
    lab = load("ch14", "l14_01_chance")
    chances = [0.3, 0.3, 0.7, 0.25, 0.35, 0.9]
    rained = [True, False, True, False, False, True]
    assert abs(lab.hit_rate(chances, rained, 0.25, 0.35) - 0.25) < 1e-12
    assert lab.hit_rate(chances, rained, 0.65, 0.75) == 1.0


def test_hit_rate_refuses_an_empty_range() -> None:
    lab = load("ch14", "l14_01_chance")
    with pytest.raises(ValueError):
        lab.hit_rate([0.1, 0.9], [True, False], 0.4, 0.6)
