__author__ = 'spacegoing'
##
import json
import os
from pprint import pprint


class ConfigReader:
    def __init__(self):
        # Read JSON Config File
        file_path = os.path.dirname(os.path.abspath(__file__))
        project_path = os.path.abspath(os.path.join(file_path, os.path.pardir))

        with open(project_path+'/Config/Daily_Scheme_Config.json') as config_file:
            self._config_file_JSON = json.load(config_file)
        # Get Configs
        self._Daily_Scheme_Config = self._config_file_JSON['Daily_Scheme_Config']

    def pprintConfigFile(self):
        pprint(self._config_file_JSON)


class DailyConfigReader(ConfigReader):
    def __init__(self):
        super().__init__()
        try:
            self._Daily_Scheme = self._Daily_Scheme_Config['DailyScheme']
            self._MISC = self._Daily_Scheme_Config['MISC']
            self._Period_Type_Params = self._Daily_Scheme_Config['Period_Type_Params']
            self._Scheme_Settings = self._Daily_Scheme_Config['Scheme_Settings']
            self._StartEnd_Symbols_Of_Day = self._Daily_Scheme_Config['StartEnd_Symbols_Of_Day']

        except KeyError as K:
            print("Error:\n Wrong Daily Configuration File:\n "
                  "The key value " + str(K) + " doesn't exist!")

    def getDaily_Scheme(self):
        """

        :return: 2 returns.
        time_Table: List. 2d list of string. [[start,end]...]
        type_Table: List. 1d list of string. ["period type",...]
        """
        time_Table = list()
        type_Table = list()
        for i in self._Daily_Scheme:
            time_Table.append([i['start'], i['end']])
            type_Table.append(i['type'])

        return time_Table, type_Table

    def getMISC(self):
        return self._MISC

    def getPeriod_Type_Params(self):
        """

        :return:
        Period_Type_Params: Dict.
        """
        return self._Period_Type_Params

    def getScheme_Settings(self):
        """

        :return: 2 returns
        Scheme_Type: String
        type_Params: Dict. Params for that shceme type.

        """
        try:
            Scheme_Type = self._Scheme_Settings['Scheme_Type']
            type_Params = self._Scheme_Settings.keys() - {'Scheme_Type'}
            Other_Params = {k: self._Scheme_Settings[k] for k in type_Params}
            return Scheme_Type, Other_Params
        except:
            print("Error:\n Missing key value 'Scheme_Type'!")

    def getStartEnd_Symbols_Of_Day(self):
        """

        :return: 2 returns
        Start_Of_Day_Symbol: String
        End_Of_Day_Symbol: String
        """
        return self._StartEnd_Symbols_Of_Day['Start_Of_Day_Symbol'], \
               self._StartEnd_Symbols_Of_Day['End_Of_Day_Symbol']

    # Return config file except 'DailyScheme' key
    def getConfigurations(self):
        ConfigurationKeys = \
            self._config_file_JSON['Daily_Scheme_Config'].keys() \
            - {'DailyScheme'}

        return {k: self._config_file_JSON['Daily_Scheme_Config'][k]
                for k in ConfigurationKeys}

##
