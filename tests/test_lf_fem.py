from qm import SimulationConfig
from qm.qua import program, play, declare, fixed, demod, measure


def test_lf_fem_single_output_port(make_qm, make_modes):
    """
    Tests that a single frequency LF-FEM output element is created for the LF-FEM.
    """
    qm = make_qm(make_modes("modes/lf_fem_single_output_port.yaml"))

    with program() as prog:
        play("test", "test")

    job = qm.simulate(prog, SimulationConfig(duration=250))
    samples = job.get_simulated_samples()
    waveform_report = job.get_simulated_waveform_report()

    config = qm.get_config()

    assert config["controllers"]["con1"]["fems"][3]["analog_outputs"][1] == {
        # defaults
        'crosstalk': {},
        'delay': 0,
        'filter': {'feedback': [], 'feedforward': []},
        'offset': 0.0,
        'output_mode': 'direct',
        'upsampling_mode': 'mw',
        # custom
        "sampling_rate": 1000000000.0,
        "shareable": False,
    }
    assert config["elements"]["test"]["singleInput"]["port"] == ('con1', 3, 1)
    assert config["elements"]["test"]["intermediate_frequency"] == 50e6

def test_lf_fem_single_input_port(make_qm, make_modes):
    """
    Tests that a single frequency LF-FEM input element is created for the LF-FEM.
    """
    qm = make_qm(make_modes("modes/lf_fem_single_input_port.yaml"))

    with program() as prog:
        I = declare(fixed)
        measure("test", "test", None, demod.full(None, I, "out1"))

    job = qm.simulate(prog, SimulationConfig(duration=250))
    samples = job.get_simulated_samples()
    waveform_report = job.get_simulated_waveform_report()

    config = qm.get_config()

    assert config["controllers"]["con1"]["fems"][3]["analog_outputs"][1] == {
        # defaults
        'crosstalk': {},
        'delay': 0,
        'filter': {'feedback': [], 'feedforward': []},
        'offset': 0.0,
        'output_mode': 'direct',
        'upsampling_mode': 'mw',
        # custom
        "sampling_rate": 1000000000.0,
        "shareable": False,
    }
    assert config["elements"]["test"]["singleInput"]["port"] == ('con1', 3, 1)
    assert config["elements"]["test"]["intermediate_frequency"] == 50e6

def test_lf_fem_and_octave_output(make_qm, make_modes):
    """
    Tests that an IQ octave output element is created for the LF-FEM.
    """
    qm = make_qm(make_modes("modes/lf_fem_iq_output_octave_port.yaml"))

    with program() as prog:
        play("test", "test")

    job = qm.simulate(prog, SimulationConfig(duration=250))
    samples = job.get_simulated_samples()
    waveform_report = job.get_simulated_waveform_report()

    config = qm.get_config()

    assert config["controllers"]["con1"]["fems"][3]["analog_outputs"][1] == {
        # defaults
        'crosstalk': {},
        'delay': 0,
        'filter': {'feedback': [], 'feedforward': []},
        'offset': 0.0,
        'output_mode': 'direct',
        'upsampling_mode': 'mw',
        # custom
        "sampling_rate": 1000000000.0,
        "shareable": False,
    }
    assert config["elements"]["test"]["RF_inputs"]["port"] == ('con1', 3, 1)
    assert config["elements"]["test"]["intermediate_frequency"] == 50e6

