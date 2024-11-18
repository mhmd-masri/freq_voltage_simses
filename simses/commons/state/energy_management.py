from simses.commons.state.abstract_state import State


class EnergyManagementState(State):
    """
    Current State of the Energy Management (PV, Load, etc..)
    """

    AC_POWER_REQUESTED = 'Power requested from EMS in W'
    LOAD_POWER = 'Load in W'
    PV_POWER = 'PV Generation in W'
    FCR_MAX_POWER = 'Power reserved for FCR in W'
    FCR_POWER = 'Power delivered for FCR in W'
    FFR_MAX_POWER = 'Power reserved for FFR in W'
    FFR_POWER = 'Power delivered for FFR in W'
    VR_MAX_POWER = 'Power reserved for VR in W'
    VR_POWER = 'Power delivered for VR in W'
    IDM_POWER = 'Power delivered for IDM in W'
    PEAKSHAVING_LIMIT = 'Peak Shaving Limit in W'
    BINARY_VALUE = 'Binary value for EVs (1 available, 0 on the road)'
    V2G_POWER = 'Power provided in V2G operation'
    FREQUENCY = 'Frequency in Hz'
    VOLTAGE = 'Voltage in pu'

    def __init__(self):
        super().__init__()
        self._initialize()

    @property
    def ac_power_requested(self) -> float:
        return self.get(self.AC_POWER_REQUESTED)

    @ac_power_requested.setter
    def ac_power_requested(self, value: float) -> None:
        self.set(self.AC_POWER_REQUESTED, value)

    @property
    def load_power(self) -> float:
        return self.get(self.LOAD_POWER)

    @load_power.setter
    def load_power(self, value: float) -> None:
        self.set(self.LOAD_POWER, value)

    @property
    def pv_power(self) -> float:
        return self.get(self.PV_POWER)

    @pv_power.setter
    def pv_power(self, value: float) -> None:
        self.set(self.PV_POWER, value)

    @property
    def binary(self) -> float:
        return self.get(self.BINARY_VALUE)

    @binary.setter
    def binary(self, value: float) -> None:
        self.set(self.BINARY_VALUE, value)

    @property
    def v2g_power(self) -> float:
        return self.get(self.V2G_POWER)

    @v2g_power.setter
    def v2g_power(self, value: float) -> None:
        self.set(self.V2G_POWER, value)

    @property
    def fcr_max_power(self) -> float:
        return self.get(self.FCR_MAX_POWER)

    @fcr_max_power.setter
    def fcr_max_power(self, value: float) -> None:
        self.set(self.FCR_MAX_POWER, value)

    @property
    def fcr_power(self) -> float:
        return self.get(self.FCR_POWER)

    @fcr_power.setter
    def fcr_power(self, value: float) -> None:
        self.set(self.FCR_POWER, value)

    @property
    def ffr_max_power(self) -> float:
        return self.get(self.FFR_MAX_POWER)

    @ffr_max_power.setter
    def ffr_max_power(self, value: float) -> None:
        self.set(self.FFR_MAX_POWER, value)


    @property
    def ffr_power(self) -> float:
        return self.get(self.FFR_POWER)

    @ffr_power.setter
    def ffr_power(self, value: float) -> None:
        self.set(self.FFR_POWER, value)
    
    @property
    def ffr_power(self) -> float:
        return self.get(self.FFR_POWER)

    @ffr_power.setter
    def fFr_power(self, value: float) -> None:
        self.set(self.FFR_POWER, value)
    
    @property
    def VR_max_power(self) -> float:
        return self.get(self.VR_MAX_POWER)

    @VR_max_power.setter
    def VR_max_power(self, value: float) -> None:
        self.set(self.VR_MAX_POWER, value)

    @property
    def VR_power(self) -> float:
        return self.get(self.VR_POWER)

    @VR_power.setter
    def VR_power(self, value: float) -> None:
        self.set(self.VR_POWER, value)

    @property
    def idm_power(self) -> float:
        return self.get(self.IDM_POWER)

    @idm_power.setter
    def idm_power(self, value: float) -> None:
        self.set(self.IDM_POWER, value)

    @property
    def peakshaving_limit(self) -> float:
        return self.get(self.PEAKSHAVING_LIMIT)

    @peakshaving_limit.setter
    def peakshaving_limit(self, value: float) -> None:
        self.set(self.PEAKSHAVING_LIMIT, value)

    @property 
    def frequency(self) -> float:
         return self.get(self.FREQUENCY)

    @frequency.setter
    def frequency(self, value: float) -> None:
        self.set(self.FREQUENCY, value)

    @property 
    def voltage(self) -> float:
         return self.get(self.VOLTAGE)

    @voltage.setter
    def voltage(self, value: float) -> None:
        self.set(self.VOLTAGE, value)

    @property
    def id(self) -> str:
        return 'EMS'

    @classmethod
    def sum_parallel(cls, system_states: []):
        raise Exception('sum_parallel is not implemented for EnergyManagementState')

    @classmethod
    def sum_serial(cls, states: []):
        raise Exception('sum_serial is not implemented for EnergyManagementState')
