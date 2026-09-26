import importlib.util
import random
from pathlib import Path

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


def test_spread_of_two_members() -> None:
    lab = load("ch14", "l14_02_saturation")
    assert lab.spread([(0.0, 0.0), (2.0, 2.0)]) == 1.0
    assert lab.spread([(1.0, 2.0, 3.0)] * 3) == 0.0


def test_saturation_on_made_up_numbers() -> None:
    lab = load("ch14", "l14_02_saturation")
    leads = [float(k) for k in range(10)]
    spreads = [0.1, 0.2, 0.5, 1.0, 2.0, 3.0, 3.5, 3.6, 3.5, 3.6]
    # plateau (3.5 + 3.6) / 2 = 3.55; nine tenths of it is 3.195
    assert lab.saturation_lead(leads, spreads) == 6.0
    assert lab.saturation_lead(leads, spreads, fraction=0.5) == 4.0


def test_the_chapters_ensemble_saturates_after_a_few_units() -> None:
    lab = load("ch14", "l14_02_saturation")
    ens = _chapter("ensemble")
    _, members = ens.ensemble(ens.spin_up(), random.Random(14))
    leads, spreads = [], []
    for k in range(161):
        leads.append(k * ens.DT)
        spreads.append(lab.spread(members))
        assert abs(spreads[-1] - ens.spread(members)) < 1e-12
        members = [ens.run(m, 1) for m in members]
    lead = lab.saturation_lead(leads, spreads)
    assert 2.5 < lead < 5.0
