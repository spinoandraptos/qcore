from pathlib import Path

from typing import Literal, Dict

import pytest

from qcore import Stage
from qcore.instruments import OPX1000, QM
from qcore.modes.mode import Mode


@pytest.fixture
def make_qm():
    def _make_qm(modes: Dict[str, Mode], settings: dict = None):
        opx1000 = OPX1000(name=Literal["opx1000"], cluster_name="CS_3", id="172.16.33.115", settings=settings)

        qm = QM(
            modes=tuple(modes.values()),
            oscillators=tuple(),
            opx=opx1000
        )
        qm = qm.open(
            modes=tuple(modes.values()),
            oscillators=tuple(),
            opx=opx1000
        )
        return qm

    return _make_qm


@pytest.fixture
def make_modes():
    def _make_modes(modes_path: str | Path):
        with Stage(modes_path) as stage:
            rscs = stage.get(*stage.resources)
            modes = {m.name: m for m in rscs if isinstance(m, Mode)}

        return modes

    return _make_modes
