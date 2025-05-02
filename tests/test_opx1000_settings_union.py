from qm import SimulationConfig, DictQuaConfig
from qm.qua import program, play, measure, dual_demod, declare, fixed


def test_mw_fem_single_output_port(make_qm, make_modes):
    """
    Tests that individual OPX1000 config parameters can be overrided by the
    OPX1000 settings attribute.

    The `settings` attribute is a partial QUA config dictionary which will
    be deep-merged into the one built from the modes. It can be used to
    override individual OPX1000 config parameters or set those which are
    not accessible through the use of Modes.
    """
    settings: DictQuaConfig = {
        "controllers": {
            "con1": {
                "fems": {
                    '1': {
                        "analog_outputs": {
                            '1': {
                                "full_scale_power_dbm": -8
                            }
                        }
                    }
                }
            }
        }
    }
    qm = make_qm(make_modes("modes/mw_fem_single_output_port.yaml"), settings=settings)

    with program() as prog:
        play("test", "test")

    job = qm.simulate(prog, SimulationConfig(duration=250))
    samples = job.get_simulated_samples()
    waveform_report = job.get_simulated_waveform_report()

    config = qm.get_config()

    assert config["controllers"]["con1"]["fems"][1]["analog_outputs"][1] == {
        # defaults
        "delay": 0,
        "full_scale_power_dbm": -8,
        "sampling_rate": 1000000000.0,
        "shareable": False,
        # configured
        "upconverters": { 1: { "frequency": 5e9 + 20e6 } },
        "band": 2
    }
    assert config["elements"]["test"]["MWInput"]["port"] == ('con1', 1, 1)
    assert config["elements"]["test"]["MWInput"]["upconverter"] == 1
    assert config["elements"]["test"]["intermediate_frequency"] == -20e6

