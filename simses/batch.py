from configparser import ConfigParser

from simses.commons.config.generation.analysis import AnalysisConfigGenerator
from simses.commons.config.generation.simulation import SimulationConfigGenerator
from simses.simulation.batch_processing import BatchProcessing


class ExampleBatchProcessing(BatchProcessing):

    """
    This is just a simple example on how to use BatchProcessing.
    """

    def __init__(self):
        super().__init__(do_simulation=True, do_analysis=True)

    def _setup_config(self) -> dict:
        # Example for config setup
        config_generator: SimulationConfigGenerator = SimulationConfigGenerator()
        # example: loading default config as base (not necessary)
        config_generator.load_local_config()

        # setting up multiple configurations with manual naming of simulations
        config_set: dict = dict()

        # sceario 1: FCR + IDM (default from config)
        config_set['scenario_1'] = config_generator.get_config()

        # scenario 2: FCR + FFR + IDM
        config_generator.set_grid_operation_strategy("FcrFfr1IdmRechargeStacked", fcr_power=2e6, ffr_power=1e6, vr_power=0.0e6, idm_power=0.9e6)
        config_set['scenario_2'] = config_generator.get_config()
        
        # scenario 3: FCR + FFR + VR + IDM
        config_generator.set_grid_operation_strategy("FcrFfrVRIdmRechargeStacked", fcr_power=1e6, ffr_power=1e6, vr_power=1e6, idm_power=0.9e6)
        config_set['scenario_3'] = config_generator.get_config()
        
        # return all scenarios
        return config_set

    def _analysis_config(self) -> ConfigParser:
        config_generator: AnalysisConfigGenerator = AnalysisConfigGenerator()
        config_generator.print_results(False)
        config_generator.do_plotting(True)
        return config_generator.get_config()

    def clean_up(self) -> None:
        pass


if __name__ == "__main__":
    batch_processing: BatchProcessing = ExampleBatchProcessing()
    batch_processing.run()
    batch_processing.clean_up()
