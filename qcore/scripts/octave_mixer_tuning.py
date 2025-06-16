from qm.QuantumMachine import QuantumMachine
from typing import List
from qcore.instruments import QM
from qcore.helpers.logger import logger
from qcore.modes.mode import Mode


class OctaveMixerTuner:


    def __init__(self, modes_to_tune: List[tuple[Mode, float, tuple[float]]], qcore_qm : QM):
        self.modes_to_tune = modes_to_tune
        self.qcore_qm = qcore_qm

    def tune_mixers(self):
        qm = self.qcore_qm._qm
        for mode_tuple in self.modes_to_tune:
            (mode,LO,IFs) = mode_tuple
            logger.info(f"Tuning {mode.name} mixers ...")
            res= qm.calibrate_element(mode.name, {LO: IFs})
        return res


