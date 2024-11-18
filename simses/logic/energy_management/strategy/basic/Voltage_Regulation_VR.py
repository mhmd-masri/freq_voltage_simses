from simses.commons.config.simulation.energy_management import EnergyManagementConfig
from simses.commons.config.simulation.general import GeneralSimulationConfig
from simses.commons.config.simulation.profile import ProfileConfig
from simses.commons.log import Logger
from simses.commons.profile.technical.frequency import FrequencyProfile
from simses.commons.profile.technical.voltage import VoltageProfile
from simses.commons.profile.technical.technical import TechnicalProfile
from simses.commons.state.energy_management import EnergyManagementState
from simses.commons.state.system import SystemState
from simses.logic.energy_management.strategy.operation_priority import OperationPriority
from simses.logic.energy_management.strategy.operation_strategy import OperationStrategy


class VR(OperationStrategy):
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
        self.__voltage: TechnicalProfile = VoltageProfile(config, profile_config)
        self.__max_VR_power = config_ems.max_VR_power 
        self.__vr_power = 0

        
        self.__VR_droop = 50  # # slope for watt-volt control
        self.__support_duration = 3600  # 1 hour for peak demand between 6 and 7 pm
        self.__recovery_period = 39600  # no service on the remaining day
        self.__counter = 0  # counter to reset the event 
        self.__t_start = None  # event start time
        self.__pout = 0  # output active power by BESS
        self.__elapsed_time = 0
        self.__event_counter_VR = 0  # Counter for voltage regulation use
        

        if config.timestep > 1:    #now we have it one minute and not second
            self.__log.warn('Timestep is > 1s. Thus, the results are distorted and are not valid. '
                             'Rethink your timestep')

    def next(self, time: float, system_state: SystemState, power: float = 0) -> float:
        voltage = self.__voltage.next(time)

        # Calculate current simulation time in hours and minutes
        current_minute = int(time) % 3600
        current_hour = (int(time) // 3600) % 24

        # Check if the current time is between 6 PM and 7 PM
        if not (18 <= current_hour < 19):
            return 0  # Outside peak hour, no regulation
        
        in_range = False

        if self.__t_start is None:
            self.__t_start = time

        # Calculate elapsed time in minutes
        self.elapsed_time = time - self.__t_start
        # Check if volt falls into any defined range and set pout accordingly
        if 0.8 < voltage <= 0.98:
            pout_value = 1
            in_range = True
        elif 0.98 < voltage <= 1:
            volt_error = voltage - 0.98
            pout_value = 1 - (self.__VR_droop * volt_error)
            in_range = True
        elif 1 < voltage <= 1.02:
            volt_error = 1.02 - voltage
            pout_value = -1 + (self.__VR_droop * volt_error)
            in_range = True
        elif 1.02 < voltage <= 1.2:
            pout_value = -1
            in_range = True
       
        
        if in_range:
            if self.__counter == 0:
                self.__t_start = time
                self.__counter += 1
                self.__event_counter_VR += 1  # Increment the event counter

            if self.__elapsed_time < self.__support_duration:
                self.__pout = pout_value
            elif self.__support_duration <= self.__elapsed_time < self.__recovery_period:
                self.__pout = 0
            elif self.__elapsed_time >= self.__recovery_period:
                self.__pout = 0
                self.__counter = 0

        else:
                if self.__elapsed_time >= self.__support_duration:
                    self.__pout = 0
                else:
                    self.__pout+=0

        p_out = - self.__pout * self.__max_VR_power
        self.__vr_power = p_out
        return p_out

    def update(self, energy_management_state: EnergyManagementState) -> None:
        energy_management_state.VR_max_power = self.__max_VR_power
        energy_management_state.VR_power = self.__vr_power

    def clear(self) -> None:
        self.__pout = 0.0

    def close(self) -> None:
        self.__voltage.close()
    
