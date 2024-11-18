from simses.commons.config.simulation.energy_management import EnergyManagementConfig
from simses.commons.config.simulation.general import GeneralSimulationConfig
from simses.commons.config.simulation.profile import ProfileConfig
from simses.commons.log import Logger
from simses.commons.profile.technical.frequency import FrequencyProfile
from simses.commons.profile.technical.technical import TechnicalProfile
from simses.commons.state.energy_management import EnergyManagementState
from simses.commons.state.system import SystemState
from simses.logic.energy_management.strategy.operation_priority import OperationPriority
from simses.logic.energy_management.strategy.operation_strategy import OperationStrategy

class FFR1(OperationStrategy):
    """
    Operation strategy for providing FFR. It was developed according to the German regulatory framework.
    The requested charging and discharging power is proportional to the frequency deviation.
    Below 49.9 Hz, the output power is set proportionally to the frequency deviation using a droop coefficient.
    """ 

    def __init__(self, config: GeneralSimulationConfig, config_ems: EnergyManagementConfig, profile_config: ProfileConfig):
        super().__init__(OperationPriority.HIGH)
        self.__log: Logger = Logger(type(self).__name__)
        self.__frequency: TechnicalProfile = FrequencyProfile(config, profile_config)
        self.__max_ffr_power = config_ems.max_ffr_power  # Watt
        self.__ffr_power = 0.0

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
        
        p_out = - self.__pout * self.__max_ffr_power
        self.__ffr_power = p_out
        return p_out

    def update(self, energy_management_state: EnergyManagementState) -> None:
        energy_management_state.ffr_max_power = self.__max_ffr_power
        energy_management_state.fcr_power = self.__ffr_power

    def clear(self) -> None:
        self.__pout = 0.0

    def close(self) -> None:
        self.__frequency.close()