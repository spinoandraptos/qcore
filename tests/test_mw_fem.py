from qm import SimulationConfig
from qm.qua import program, play, measure, dual_demod, declare, fixed


def test_mw_fem_single_output_port(make_qm, make_modes):
    """
    Tests that a single 5GHz frequency output element is created with the following configuration:
     - LO = +20MHz + 5GHz buffer by default
     - IF = -20MHz
     - port = (con1, 1, 1)
    """
    qm = make_qm(make_modes("modes/mw_fem_single_output_port.yaml"))

    with program() as prog:
        play("test", "test")

    job = qm.simulate(prog, SimulationConfig(duration=250))
    samples = job.get_simulated_samples()
    waveform_report = job.get_simulated_waveform_report()

    config = qm.get_config()

    assert config["controllers"]["con1"]["fems"][1]["analog_outputs"][1] == {
        # defaults
        "delay": 0,
        "full_scale_power_dbm": -11,
        "sampling_rate": 1000000000.0,
        "shareable": False,
        # configured
        "upconverters": { 1: { "frequency": 5e9 + 20e6 } },
        "band": 2
    }
    assert config["elements"]["test"]["MWInput"]["port"] == ('con1', 1, 1)
    assert config["elements"]["test"]["MWInput"]["upconverter"] == 1
    assert config["elements"]["test"]["intermediate_frequency"] == -20e6


def test_mw_fem_single_input_port(make_qm, make_modes):
    """
    Tests that a single 5GHz frequency input element is created with the following configuration:
     - LO = +20MHz + 5GHz buffer by default
     - IF = -20MHz
     - port = (con1, 1, 1)
    """
    qm = make_qm(make_modes("modes/mw_fem_single_input_port.yaml"))

    with program() as prog:
        I, Q = declare(fixed), declare(fixed)
        measure("test", "test", None, dual_demod.full('cos', 'sin', I), dual_demod.full('minus_sin', 'cos', Q))

    job = qm.simulate(prog, SimulationConfig(duration=250))
    samples = job.get_simulated_samples()
    waveform_report = job.get_simulated_waveform_report()

    config = qm.get_config()

    assert config["controllers"]["con1"]["fems"][1]["analog_inputs"][1] == {
        # defaults
        'gain_db': 0,
        'sampling_rate': 1000000000.0,
        'shareable': False,
        # configured
        "downconverter_frequency": 5e9 + 20e6,
        "band": 2
    }
    assert config["controllers"]["con1"]["fems"][1]["analog_outputs"][1] == {
        # defaults
        "delay": 0,
        "full_scale_power_dbm": -11,
        "sampling_rate": 1000000000.0,
        "shareable": False,
        # configured
        "upconverters": { 1: { "frequency": 5e9 + 20e6 } },
        "band": 2
    }
    assert config["elements"]["test"]["MWInput"]["port"] == ('con1', 1, 1)
    assert config["elements"]["test"]["MWInput"]["upconverter"] == 1
    assert config["elements"]["test"]["intermediate_frequency"] == -20e6


def test_mw_fem_dual_output_same_duc_close_frequencies(make_qm, make_modes):
    """
    Tests that two very similar-frequency output elements are created with the following configuration:
     - LO = nearest allowed value, i.e., at least 20MHz away from nearest frequency
     - IF = corresponding LOs
     - port = (con1, 1, 1)
    """
    qm = make_qm(make_modes("modes/mw_fem_dual_output_same_duc_close_frequencies.yaml"))

    with program() as prog:
        play("test", "test1")
        play("test", "test2")

    job = qm.simulate(prog, SimulationConfig(duration=250))
    samples = job.get_simulated_samples()
    waveform_report = job.get_simulated_waveform_report()

    config = qm.get_config()

    assert config["controllers"]["con1"]["fems"][1]["analog_outputs"][1] == {
        # defaults
        "delay": 0,
        "full_scale_power_dbm": -11,
        "sampling_rate": 1000000000.0,
        "shareable": False,
        # configured
        "upconverters": { 1: { "frequency": 5.05e9 } },
        "band": 2
    }
    assert config["elements"]["test1"]["MWInput"]["port"] == ('con1', 1, 1)
    assert config["elements"]["test1"]["MWInput"]["upconverter"] == 1
    assert config["elements"]["test1"]["intermediate_frequency"] == -50e6
    assert config["elements"]["test2"]["MWInput"]["port"] == ('con1', 1, 1)
    assert config["elements"]["test2"]["MWInput"]["upconverter"] == 1
    assert config["elements"]["test2"]["intermediate_frequency"] == -20e6


def test_mw_fem_dual_output_same_duc(make_qm, make_modes):
    """
    Tests that two similar-frequency output elements are created with the following configuration:
     - LO = average of both elements
     - IF = corresponding LOs
     - port = (con1, 1, 1)
    """
    qm = make_qm(make_modes("modes/mw_fem_dual_output_same_duc.yaml"))

    with program() as prog:
        play("test", "test1")
        play("test", "test2")

    job = qm.simulate(prog, SimulationConfig(duration=250))
    samples = job.get_simulated_samples()
    waveform_report = job.get_simulated_waveform_report()

    config = qm.get_config()

    assert config["controllers"]["con1"]["fems"][1]["analog_outputs"][1] == {
        # defaults
        "delay": 0,
        "full_scale_power_dbm": -11,
        "sampling_rate": 1000000000.0,
        "shareable": False,
        # configured
        "upconverters": { 1: { "frequency": 5.05e9 } },
        "band": 2
    }
    assert config["elements"]["test1"]["MWInput"]["port"] == ('con1', 1, 1)
    assert config["elements"]["test1"]["MWInput"]["upconverter"] == 1
    assert config["elements"]["test1"]["intermediate_frequency"] == -50e6
    assert config["elements"]["test2"]["MWInput"]["port"] == ('con1', 1, 1)
    assert config["elements"]["test2"]["MWInput"]["upconverter"] == 1
    assert config["elements"]["test2"]["intermediate_frequency"] == +50e6


def test_mw_fem_dual_output_different_duc(make_qm, make_modes):
    """
    Tests that two separated frequency output elements are created with the following configuration:
     - 2x DUCs
     - IF = DUC - 20MHz
     - port = (con1, 1, 1)
    """
    qm = make_qm(make_modes("modes/mw_fem_dual_output_different_duc.yaml"))

    with program() as prog:
        play("test", "test1")
        play("test", "test2")

    job = qm.simulate(prog, SimulationConfig(duration=250))
    samples = job.get_simulated_samples()
    waveform_report = job.get_simulated_waveform_report()

    config = qm.get_config()

    assert config["controllers"]["con1"]["fems"][1]["analog_outputs"][1] == {
        # defaults
        "delay": 0,
        "full_scale_power_dbm": -11,
        "sampling_rate": 1000000000.0,
        "shareable": False,
        # configured
        "upconverters": {
            1: { "frequency": 5.0e9 + 20e6},
            2: {"frequency": 6.1e9 + 20e6}
        },
        "band": 2
    }
    assert config["elements"]["test1"]["MWInput"]["port"] == ('con1', 1, 1)
    assert config["elements"]["test1"]["MWInput"]["upconverter"] == 1
    assert config["elements"]["test1"]["intermediate_frequency"] == -20e6
    assert config["elements"]["test2"]["MWInput"]["port"] == ('con1', 1, 1)
    assert config["elements"]["test2"]["MWInput"]["upconverter"] == 2
    assert config["elements"]["test2"]["intermediate_frequency"] == -20e6


def test_mw_fem_dual_input_ports(make_qm, make_modes):
    """
    Tests that two readout elements are created with the following configuration:
     - LO = same LO, average of both frequencies
     - IF = correct IFs
     - port = (con1, 1, 1)
    """
    qm = make_qm(make_modes("modes/mw_fem_dual_input_port.yaml"))

    with program() as prog:
        I, Q = declare(fixed), declare(fixed)
        measure("test", "test1", None, dual_demod.full('cos', 'sin', I), dual_demod.full('minus_sin', 'cos', Q))
        measure("test", "test2", None, dual_demod.full('cos', 'sin', I), dual_demod.full('minus_sin', 'cos', Q))

    job = qm.simulate(prog, SimulationConfig(duration=250))
    samples = job.get_simulated_samples()
    waveform_report = job.get_simulated_waveform_report()

    config = qm.get_config()

    assert config["controllers"]["con1"]["fems"][1]["analog_inputs"][1] == {
        # defaults
        'gain_db': 0,
        'sampling_rate': 1000000000.0,
        'shareable': False,
        # configured
        "downconverter_frequency": 5.05e9,
        "band": 2
    }
    assert config["controllers"]["con1"]["fems"][1]["analog_outputs"][1] == {
        # defaults
        "delay": 0,
        "full_scale_power_dbm": -11,
        "sampling_rate": 1000000000.0,
        "shareable": False,
        # configured
        "upconverters": { 1: { "frequency": 5.05e9 } },
        "band": 2
    }
    assert config["elements"]["test1"]["MWInput"]["port"] == ('con1', 1, 1)
    assert config["elements"]["test1"]["MWInput"]["upconverter"] == 1
    assert config["elements"]["test1"]["intermediate_frequency"] == -50e6

    assert config["elements"]["test2"]["MWInput"]["port"] == ('con1', 1, 1)
    assert config["elements"]["test2"]["MWInput"]["upconverter"] == 1
    assert config["elements"]["test2"]["intermediate_frequency"] == -20e6
