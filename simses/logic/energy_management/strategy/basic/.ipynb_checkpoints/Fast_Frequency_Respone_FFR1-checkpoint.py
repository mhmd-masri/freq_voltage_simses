# from simses.commons.config.simulation.energy_management import EnergyManagementConfig
# from simses.commons.config.simulation.general import GeneralSimulationConfig
# from simses.commons.config.simulation.profile import ProfileConfig
# from simses.commons.log import Logger
# from simses.commons.profile.technical.frequency import FrequencyProfile
# from simses.commons.profile.technical.technical import TechnicalProfile
# from simses.commons.state.energy_management import EnergyManagementState
# from simses.commons.state.system import SystemState
# from simses.logic.energy_management.strategy.operation_priority import OperationPriority
# from simses.logic.energy_management.strategy.operation_strategy import OperationStrategy

# +
class FFR1(OperationStrategy):
    """
    Operation strategy for providing FCR. It was developed according to the German regulatory framework .
    The requested charging and discharging power is proportional to the frequency deviation.
    Below 49.8 Hz or above 50.2 Hz the output power is set to the prequalified power. Within the frequency dead band
    around 50 Hz with +/-10 mHz the output power is set to 0 W. The degree of freedom to exceed the output power by a
    factor of 1.2 is used aiming to bring the SOC back to a predefined SOC set point. --> change this to describe FFR1???
    """ 

def __init__(self, config: GeneralSimulationConfig, config_ems: EnergyManagementConfig, profile_config: ProfileConfig):
        super().__init__(OperationPriority.HIGH)
        self.__log: Logger = Logger(type(self).__name__)
        self.__frequency: TechnicalProfile = FrequencyProfile(config, profile_config)
        self.__max_fcr_power = config_ems.max_fcr_power  # Watt (shall we have the same for FFR1, shall we adjust?)
        self.__soc_set = config_ems.soc_set  # pu (delete)

        self.__nominal_frequency = 50.0  # Hz
        self.__fUF_FFR1 = 49.9  # Hz
        self.__support_duration = 30  # s
        self.__recovery_period = 300  # s
        self.__kUF_FFR1 = 0.05  # droop coefficient
        self.__counter = 0  # counter to reset the event 
        self.__t_start = 0  # event start time
        self.__pout = 0  # output active power by BESS  
        self.__event_counter_FFR1 = 0  # Counter for frequency drops below 49.9Hz
        

        if config.timestep > 1:
            self.__log.warn('Timestep is > 1s. Thus, the results are distorted and are not valid. '
                             'Rethink your timestep')

    def next(self, time: float, system_state: SystemState, power: float = 0) -> float:
        frequency = self.__frequency.next(time)

        if frequency < self.__fUF_FFR1:
            if self.__counter ==0:
                self.__t_start = time
                self.__counter += 1
                self.__event_counter_FFR1 += 1 # Increment the event counter
            
            if (time - self.__t_start) < self.__support_duration:
                self.__pout = max(0, (self.__fUF_FFR1 - frequency) / (self.__nominal_frequency * self.__kUF_FFR1))
            elif self.__support_duration <= (time - self.__t_start) < self.__recovery_period:
                self.__pout = 0
            elif (time - self.__t_start) >= self.__recovery_period:
                self.__pout = 0
                self.__counter = 0
                
        else:
            self.__pout = 0
            
        return self.__pout

    def update(self, energy_management_state: EnergyManagementState) -> None:
        energy_management_state.fcr_max_power = self.__max_fcr_power #should we add in the energy management ffr???

    def clear(self) -> None:
        self.__power_fcr_last_step = 0.0 #we already putting pout = 0 in the end??? do we need it?

    def close(self) -> None:
        self.__frequency.close()
