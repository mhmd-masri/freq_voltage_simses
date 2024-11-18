from ast import literal_eval
from configparser import ConfigParser
from simses.commons.state.parameters import SystemParameters


class SystemParametersReader:
    """
    SystemParametersReader provides a third interface to SimSES for external programs which need to access variables
    whose values are known only after the SimSES object has been instantiated.
    This class reads the SystemParameters.txt file generated by the SimSES constructor after instantiation, and provides
    specific values contained therein.
    An example of one such variable: the number of containers

    """

    def __init__(self, path: str, name: str = None):
        config: ConfigParser = ConfigParser()
        if name:
            file_path = path + name + '/' + SystemParameters.get_file_name()
        else:
            file_path = path + SystemParameters.get_file_name()
        config.read(file_path)
        self.__system_parameters: dict = literal_eval(config.get(SystemParameters.SECTION, SystemParameters.PARAMETERS))

    def get_all_storage_systems_ac(self) -> [dict]:  # TODO consider if this should be a private method
        """
        Obtaining all StorageSystemAC objects in system
        :return: System parameters of all StorageSystemAC objects created as a list of dict
        """
        return self.__system_parameters[SystemParameters.SUBSYSTEM]

    def get_number_of_storage_systems_ac(self) -> int:
        """
        Obtaining number of StorageSystemAC objects in system
        :return: number of StorageSystemAC objects created as int
        """
        return len(self.get_all_storage_systems_ac())

    def get_storage_system_ac_id_for(self, system: dict) -> int:
        return int(system[SystemParameters.ID])

    def get_storage_system_ac(self, id: int) -> dict:  # TODO consider if this should be a private method
        """
        Querying a StorageSystemAC object by ID
        :param id: ID of the StorageSystemAC object to be queried as int
        :return: attributes of the queried StorageSystemAC object as a dict
        """
        systems: dict = self.get_all_storage_systems_ac()
        for system in systems:
            if self.get_storage_system_ac_id_for(system) == id:
                return system
        raise Exception('Requested storage system AC not available.')

    def get_container_type_for(self, id: int) -> str:
        """
        Query the Housing object type for specified StorageSystemAC object
        :param id: ID of the StorageSystemAC object to be queried as int
        :return: name of the container Housing object type as str
        """
        system: dict = self.get_storage_system_ac(id)
        type: str = system[SystemParameters.CONTAINER_TYPE]
        return type

    def get_number_of_containers_for(self, id: int) -> int:
        """
        Query the number of container for specified StorageSystemAC object
        :param id: ID of the StorageSystemAC object to be queried as int
        :return: number of containers in the StorageSystemAC object as int
        """
        system: dict = self.get_storage_system_ac(id)
        number_containers = system[SystemParameters.CONTAINER_NUMBER]
        return number_containers

    def get_total_containers(self) -> int:
        """
        Obtain the total number of containers for all StorageSystemAC objects in system
        :return: total number of containers as int
        """
        total_number_containers: int = 0
        systems: [dict] = self.get_all_storage_systems_ac()
        for system in systems:
            system_id: int = self.get_storage_system_ac_id_for(system)
            if self.get_number_of_containers_for(system_id) > 0:
                print(system[SystemParameters.SYSTEM] + ' ' + str(system_id) +
                      ' has ' + str(self.get_number_of_containers_for(system_id)) + ' container(s) of type '
                      + self.get_container_type_for(system_id))
                total_number_containers += self.get_number_of_containers_for(system_id)
            else:
                print(system[SystemParameters.SYSTEM] + ' ' + str(system_id) +
                      ' has ' + self.get_container_type_for(system_id))
        return total_number_containers

    def get_acdc_converter_type_for(self, id: int) -> str:
        """
        Query the ACDC Converter object type for specified StorageSystemAC object
        :param id: ID of the StorageSystemAC object to be queried as int
        :return: name of the ACDC Converter object type as str
        """
        system: dict = self.get_storage_system_ac(id)
        type: str = system[SystemParameters.ACDC_CONVERTER]
        return type

    def get_all_storage_systems_dc_for(self, id: int) -> [dict]:  # TODO consider if this should be a private method
        """
        Obtaining all StorageSystemDC objects in specified StorageSystemAC
        :param id: id of StorageSystemAC
        :return: System parameters of all StorageSystemDC objects as a list of dict
        """
        system: dict= self.get_storage_system_ac(id)
        dc_systems: [dict] = system[SystemParameters.SUBSYSTEM]
        return dc_systems

    def get_number_of_storage_systems_dc(self, id: int) -> int:
        """
        Obtain number of StorageSystemDC objects in specified StorageSystemAC
        :param id: ID of the StorageSystemAC object to be queried as int
        :return: number of StorageSystemDC objects in specified StorageSystemAC as int
        """
        return len(self.get_all_storage_systems_dc_for(id))

    def get_storage_system_dc_str_id_for(self, system: dict) -> str:
        """
        Returns the ID of the provided StorageSystemDC as str with the ID of StorageSystemAC
        :param system: StorageSystemDC as dict
        :return: ID of the provided StorageSystemDC as str
        """
        return str(system[SystemParameters.ID])

    def get_storage_system_dc_id_for(self, system: dict) -> int:
        """
        Returns the ID of the provided StorageSystemDC as int without the ID of StorageSystemAC
        :param system: StorageSystemDC as dict
        :return: ID of the provided StorageSystemDC as int
        """
        str_id = self.get_storage_system_dc_str_id_for(system)
        id = int(float(str_id.split('.')[1]))
        return id

    def get_storage_system_dc(self, ac_id: int, dc_id: int) -> dict:  # TODO consider if this should be a private method
        """
        Query a StorageSystemDC object by StorageSystemAC ID and StorageSystemDC ID
        :param dc_id_str: ID of the StorageSystemDC object to be queried as str (also contains the StorageSystemAC ID)
        :param ac_id: ID of the StorageSystemAC object to be queried as int
        :param dc_id: ID of the StorageSystemDC object to be queried as int
        :return: attributes of the queried StorageSystemDC object as dict
        """
        systems: dict = self.get_all_storage_systems_dc_for(ac_id)
        system_id = str(ac_id) + '.' + str(dc_id)
        for system in systems:
            if self.get_storage_system_dc_str_id_for(system) == system_id:
                return system
        raise Exception('Requested storage system DC not available.')

    def get_dcdc_converter_type_for(self, ac_id: int, dc_id: int) -> str:
        """
        Query the DCDC Converter object type for specified StorageSystemDC object
        :param ac_id: ID of the StorageSystemAC object to be queried as int
        :param dc_id: ID of the StorageSystemDC object to be queried as int
        :return: name of the DCDC Converter object type as str
        """
        system: dict = self.get_storage_system_dc(ac_id, dc_id)
        type: str = system[SystemParameters.DCDC_CONVERTER]
        return type

    def get_storage_technology_for(self, ac_id: int, dc_id: int) -> str:
        """
        Query the Storage Technology object type for specified StorageSystemDC object
        :param ac_id: ID of the StorageSystemAC object to be queried as int
        :param dc_id: ID of the StorageSystemDC object to be queried as int
        :return: name of the Storage Technology object type as str
        """
        system: dict = self.get_storage_system_dc(ac_id, dc_id)
        type: str = system[SystemParameters.STORAGE_TECHNOLOGY]
        return type

    def get_cell_type_for(self, ac_id: int, dc_id: int) -> str:
        """
        Query the Cell type for specified StorageSystemDC object
        :param ac_id: ID of the StorageSystemAC object to be queried as int
        :param dc_id: ID of the StorageSystemDC object to be queried as int
        :return: name of the Cell type as str
        """
        system: dict = self.get_storage_system_dc(ac_id, dc_id)
        type: str = system[SystemParameters.CELL_TYPE]
        return type

    def get_battery_circuit_for(self, ac_id: int, dc_id: int) -> str:
        """
        Query the Battery Circuit for specified StorageSystemDC object
        :param ac_id: ID of the StorageSystemAC object to be queried as int
        :param dc_id: ID of the StorageSystemDC object to be queried as int
        :return: Battery Circuit as str
        """
        system: dict = self.get_storage_system_dc(ac_id, dc_id)
        circuit: str = system[SystemParameters.BATTERY_CIRCUIT]
        return circuit

    def get_auxiliaries_for(self, id: int) -> [str]:
        """
        Query the Auxiliary Components for specified StorageSystemDC object.
        :param id: ID of the StorageSystemAC object to be queried as int
        :return: list of auxiliary components as list of str
        """
        system: dict= self.get_storage_system_ac(id)
        auxiliaries: [str] = system[SystemParameters.AUXILIARIES]
        return auxiliaries

    def get_all_acdc_converters(self) -> [str]:  # TODO consider if this should be a private method
        """
        Query all ACDC Converter objects
        :return: Names of all DCDC Converter objects as list of str
        """
        systems: dict = self.get_all_storage_systems_ac()
        acdc_converters: [str] = list()
        for system in systems:
            acdc_converters.append(self.get_acdc_converter_type_for(self.get_storage_system_ac_id_for(system)))
        return acdc_converters

    def get_all_auxiliaries(self) -> [list]:  # TODO consider if this should be a private method
        """
        Query all Auxiliary System objects in specified StorageSystemAC
        :return: Names of all Auxiliary System objects in specified StorageSystemAC as list of str
        """
        systems: dict = self.get_all_storage_systems_ac()
        auxiliaries: [list] = list()
        for system in systems:
            auxiliaries.append(self.get_auxiliaries_for(self.get_storage_system_ac_id_for(system)))
        return auxiliaries

    def get_all_dcdc_converters(self, ac_id: int) -> [str]:  # TODO consider if this should be a private method
        """
        Query all DCDC Converter objects in specified StorageSystemAC
        :param ac_id: ID of StorageSystemAC
        :return: Names of all DCDC Converter objects in specified StorageSystemAC as list of str
        """
        dc_systems = self.get_all_storage_systems_dc_for(ac_id)
        dcdc_converters: [str] = list()
        for dc_system in dc_systems:
            dc_id: int = self.get_storage_system_dc_id_for(dc_system)
            dcdc_converters.append(self.get_dcdc_converter_type_for(ac_id, dc_id))
        return dcdc_converters






