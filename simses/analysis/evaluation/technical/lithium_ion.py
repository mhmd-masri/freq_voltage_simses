import numpy as np
from simses.analysis.data.lithium_ion import LithiumIonData
from simses.analysis.evaluation.plotting.axis import Axis
from simses.analysis.evaluation.plotting.plotly_plotting import PlotlyPlotting
from simses.analysis.evaluation.plotting.plotter import Plotting
from simses.analysis.evaluation.result import EvaluationResult, Description, Unit
from simses.analysis.evaluation.technical.technical_evaluation import TechnicalEvaluation
from simses.commons.config.analysis.general import GeneralAnalysisConfig
from simses.commons.config.simulation.battery import BatteryConfig
from simses.commons.state.technology.lithium_ion import LithiumIonState

class LithiumIonTechnicalEvaluation(TechnicalEvaluation):

    __title_overview = 'SOC, internal resistance, temperature and capacity'
    __title_current = 'Current and voltage'
    __title_degradation = 'Degradation of capacity and increase of internal resistance'

    def __init__(self, data: LithiumIonData, config: GeneralAnalysisConfig, battery_config: BatteryConfig, path: str):
        super().__init__(data, config)
        title_extension: str = ' for lithium-ion system ' + self.get_data().id
        self.__title_overview += title_extension
        self.__title_current += title_extension
        self.__title_degradation += title_extension
        self.__result_path = path

    def evaluate(self):
        super().evaluate()
        self.append_result(EvaluationResult(Description.Technical.EQUIVALENT_FULL_CYCLES, Unit.NONE, self.equivalent_full_cycles))
        self.append_result(EvaluationResult(Description.Technical.DEPTH_OF_DISCHARGE, Unit.PERCENTAGE, self.depth_of_discharges))
        self.append_result(EvaluationResult(Description.Technical.STORAGE_TECHNOLOGY_TEMPORAL_UTILIZATION, Unit.NONE, self.storage_technology_temporal_utilization))
        self.append_result((EvaluationResult(Description.Technical.C_RATE_CHARGING, Unit.ONE_PER_HOUR, self.c_rate_mean_charge)))
        self.append_result((EvaluationResult(Description.Technical.C_RATE_DISCHARGING, Unit.ONE_PER_HOUR, self.c_rate_mean_discharge)))

        # self.append_result(EvaluationResult(Description.Technical.ENERGY_THROUGHPUT, Unit.KWH, self.energy_throughput))
        # self.append_time_series(LithiumIonState.VOLTAGE, self.get_data().voltage)
        self.print_results()

    @property
    def c_rate_mean_charge(self) -> float:

        """
        Calculates the average c-rate while charging

        Parameters
        ----------
            data : simulation results

        Returns
        -------
        float:
            mean c-rate when charging
        """
        data: LithiumIonData = self.get_data()
        charge_current_mean = np.mean(data.current[data.current > 0])
        battery_energy = 1000*data.initial_capacity # in Wh

        nominal_voltage = float(data.nominal_voltage)
        battery_capacity_ah = battery_energy/nominal_voltage
        c_rate_charging = charge_current_mean / battery_capacity_ah

        charge_power_mean = np.mean(data.power[data.power > 0])
        e_rate_charging = charge_power_mean/battery_energy # based on power and energy instead of current and capacity

        return c_rate_charging

    @property
    def c_rate_mean_discharge(self) -> float:

        """
        Calculates the average c-rate while discharging

        Parameters
        ----------
            data : simulation results

        Returns
        -------
        float:
            mean c-rate when discharging
        """
        data: LithiumIonData = self.get_data()
        discharge_current_mean = np.mean(data.current[data.current < 0])
        battery_energy = 1000*data.initial_capacity # in Wh

        nominal_voltage = data.nominal_voltage
        battery_capacity_ah = battery_energy / nominal_voltage
        c_rate_discharging = -discharge_current_mean / battery_capacity_ah

        discharge_power_mean = np.mean(data.power[data.power < 0])
        e_rate_discharging = -discharge_power_mean/battery_energy # based on power and energy instead of current and capacity

        return c_rate_discharging


    def plot(self) -> None:
        self.__plot_overview()
        self.__plot_current_voltage()
        self.__plot_degradation()

    def __plot_overview(self) -> None:
        data: LithiumIonData = self.get_data()
        plot: Plotting = PlotlyPlotting(title=self.__title_overview, path=self.__result_path)
        xaxis: Axis = Axis(data=Plotting.format_time(data.time), label=LithiumIonState.TIME)
        yaxis: [Axis] = list()
        yaxis.append(Axis(data=data.soc, label=LithiumIonState.SOC, color=PlotlyPlotting.Color.SOC_BLUE,
                          linestyle=PlotlyPlotting.Linestyle.SOLID))
        yaxis.append(Axis(data=data.capacity * 1000, label=LithiumIonState.CAPACITY,
                          color=PlotlyPlotting.Color.SOH_GREEN, linestyle=PlotlyPlotting.Linestyle.SOLID))
        yaxis.append(Axis(data=data.resistance, label=LithiumIonState.INTERNAL_RESISTANCE,
                          color=PlotlyPlotting.Color.RESISTANCE_BLACK, linestyle=PlotlyPlotting.Linestyle.SOLID))
        yaxis.append(Axis(data=data.temperature, label=LithiumIonState.TEMPERATURE,
                          color=PlotlyPlotting.Color.TEMPERATURE_RED, linestyle=PlotlyPlotting.Linestyle.SOLID))
        plot.subplots(xaxis=xaxis, yaxis=yaxis)
        self.extend_figures(plot.get_figures())

    def __plot_current_voltage(self) -> None:
        data: LithiumIonData = self.get_data()
        plot: Plotting = PlotlyPlotting(title=self.__title_current, path=self.__result_path)
        xaxis: Axis = Axis(data=Plotting.format_time(data.time), label=LithiumIonState.TIME)
        yaxis: [Axis] = list()
        yaxis.append(Axis(data=data.current, label=LithiumIonState.CURRENT,
                          color=PlotlyPlotting.Color.RESISTANCE_BLACK, linestyle=PlotlyPlotting.Linestyle.SOLID))
        yaxis.append(Axis(data=data.voltage, label=LithiumIonState.VOLTAGE,
                          color=PlotlyPlotting.Color.TEMPERATURE_RED, linestyle=PlotlyPlotting.Linestyle.SOLID))
        plot.lines(xaxis=xaxis, yaxis=yaxis, secondary=[1])
        self.extend_figures(plot.get_figures())

    def __plot_degradation(self) -> None:
        data: LithiumIonData = self.get_data()
        plot: Plotting = PlotlyPlotting(title=self.__title_degradation, path=self.__result_path)
        xaxis: Axis = Axis(data=Plotting.format_time(data.time), label=LithiumIonState.TIME)
        yaxis: [Axis] = list()
        yaxis.append(Axis(data=data.capacity_loss_calendar, label=LithiumIonState.CAPACITY_LOSS_CALENDRIC,
                          color=PlotlyPlotting.Color.DC_POWER_GREEN,
                          linestyle=PlotlyPlotting.Linestyle.SOLID))
        yaxis.append(Axis(data=data.capacity_loss_cyclic, label=LithiumIonState.CAPACITY_LOSS_CYCLIC,
                          color=PlotlyPlotting.Color.AC_POWER_BLUE,
                          linestyle=PlotlyPlotting.Linestyle.SOLID))
        yaxis.append(Axis(data=data.resistance_increase_calendar, label=LithiumIonState.RESISTANCE_INCREASE_CALENDRIC,
                          color=PlotlyPlotting.Color.RED,
                          linestyle=PlotlyPlotting.Linestyle.SOLID))
        yaxis.append(Axis(data=data.resistance_increase_cyclic, label=LithiumIonState.RESISTANCE_INCREASE_CYCLIC,
                          color=PlotlyPlotting.Color.GREEN,
                          linestyle=PlotlyPlotting.Linestyle.SOLID))
        # plot.lines(xaxis=xaxis, yaxis=yaxis, secondary=[2, 3])
        plot.bar(yaxis=yaxis, bars=int(len(yaxis) / 2))
        self.extend_figures(plot.get_figures())

    # @property
    # def capacity_remaining(self) -> float:
    #     data: LithiumIonData = self.get_data()
    #     return data.state_of_health[-1] * 100
