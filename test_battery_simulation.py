import pybamm
import pytest

def test_battery_simulation():
    # Creating an experiment
    experiment = pybamm.Experiment(
        [
            "Discharge at C/10 for 10 hours",
            "Rest for 1 hour",
            "Charge at 1A until 4.1 V",
            "Hold at 4.1 V until 50mA",
            "Rest for 1 hour",
        ]
        * 3
    )

    # Creating a lithium-ion battery model
    model = pybamm.lithium_ion.DFN()

    # Creating a simulation
    sim = pybamm.Simulation(
        model,
        experiment=experiment,
        solver=pybamm.CasadiSolver(),
    )

    # Solving the simulation
    sim.solve()

    # Check the results using pytest assertions
    terminal_voltage = sim.solution["Terminal voltage [V]"]
    assert len(terminal_voltage.entries) > 0  # Check if there are data points
    final_voltage = terminal_voltage.entries[-1]  # Corrected access to the final voltage

    # Adjust the expected value and tolerance
    expected_voltage = 4.1  
    tolerance = 0.01  # 

    assert final_voltage == pytest.approx(expected_voltage, rel=tolerance)

if __name__ == "__main__":
    pytest.main()
