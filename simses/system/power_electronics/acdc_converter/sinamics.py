import math

import pandas as pd

from simses.commons.config.data.power_electronics import PowerElectronicsConfig
from simses.commons.log import Logger
from simses.commons.utils.utilities import check
from simses.system.power_electronics.acdc_converter.abstract_acdc_converter import AcDcConverter


class Sinamics120AcDcConverter(AcDcConverter):
    """This class uses a pre-generated Look-up table (LUT) for the efficiency of the Sinamics S120 converter in charging
    and discharging processes. The LUT was generated by Michael Schimpe from measured data using a script written in
    MATLAB. The efficiency is measured for 650 V. Source: https://doi.org/10.1016/j.egypro.2018.11.065 """

    """https://new.siemens.com/global/de/produkte/antriebstechnik/umrichter.html"""

    __VOLUMETRIC_POWER_DENSITY = 143 * 1e6  # W / m3
    __GRAVIMETRIC_POWER_DENSITY = 17000  # W/kg
    __SPECIFIC_SURFACE_AREA = 0.0001  # in m2 / W  # TODO add exact values
    # Exemplary value from:
    # (https://www.iisb.fraunhofer.de/en/research_areas/vehicle_electronics/dcdc_converters/High_Power_Density.html)
    # ( https://www.apcuk.co.uk/app/uploads/2018/02/PE_Full_Pack.pdf )

    def __init__(self, max_power: float, config: PowerElectronicsConfig):
        super().__init__(max_power)
        __filename = config.sinamics_efficiency_file
        self.__efficiency = pd.read_csv(__filename)  # pu
        self.__log: Logger = Logger(type(self).__name__)

    def to_ac(self, power: float, voltage: float) -> float:
        check(power)
        res: float = 0.0
        if power < 0.0:
            power_factor = abs(power) / self.max_power
            res = power / self.__get_efficiency(power, power_factor)
        return res

    def to_dc(self, power: float, voltage: float) -> float:
        check(power)
        res: float = 0.0
        if power > 0.0:
            power_factor = abs(power) / self.max_power
            res = power * self.__get_efficiency(power, power_factor)
        return res

    def to_dc_reverse(self, dc_power: float, voltage: float) -> float:
        check(dc_power)
        res: float = 0.0
        if dc_power > 0.0:
            power_factor = min(abs(dc_power) / (self.max_power * self.__efficiency.iloc[-1, 0]), 1.0)
            res = dc_power / self.__get_efficiency(dc_power, power_factor)
        return res

    def to_ac_reverse(self, dc_power: float, voltage: float) -> float:
        check(dc_power)
        res: float = 0.0
        if dc_power < 0.0:
            power_factor = min(abs(dc_power) / (self.max_power * self.__efficiency.iloc[-1, 1]), 1.0)
            res = dc_power * self.__get_efficiency(dc_power, power_factor)
        return res

    def __get_efficiency(self, power: float, power_factor: float) -> float:
        if power_factor < 0.0 or power_factor > 1.0:
            raise Exception('Power factor is not possible: ' + str(power_factor))
        power_factor = int(round(power_factor * 1000))
        if power_factor > 0:
            if power > 0: # charging
                return self.__efficiency.iloc[power_factor, 0]
            elif power < 0: # discharging
                return self.__efficiency.iloc[power_factor, 1]
        else:
            return math.inf

    @property
    def volume(self) -> float:
        return self.max_power / self.__VOLUMETRIC_POWER_DENSITY

    @property
    def mass(self):
        return self.max_power / self.__GRAVIMETRIC_POWER_DENSITY

    @property
    def surface_area(self) -> float:
        return self.max_power * self.__SPECIFIC_SURFACE_AREA

    @classmethod
    def create_instance(cls, max_power: float, power_electronics_config: PowerElectronicsConfig):
        return Sinamics120AcDcConverter(max_power, power_electronics_config)

    def close(self) -> None:
        pass
