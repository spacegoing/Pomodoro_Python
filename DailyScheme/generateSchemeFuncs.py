__author__ = 'spacegoing'
##
import json
import os
from DailyScheme.readConfigFuncs import DailyConfigReader
from DailyScheme.Pomo_Scheme import pomo_Gen_Execute_Plan

# Below are all global variables
file_path = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.abspath(os.path.join(file_path, os.path.pardir))

# Todo: Change to parameters or write in configuration files
types_To_Apply_Pomo = ['Work']

short_Break_Mode = 'pomo_Short_Break_Mode'
long_Break_Mode = 'pomo_Long_Break_Mode'
work_Mode = 'pomo_Work_Mode'
stop_Mode = 'pomo_Stop_Mode'
pomo_Modes = [short_Break_Mode, long_Break_Mode, work_Mode, stop_Mode]


def scheme_Writter(name, type, Execute_Plan, configurations):
    Scheme = dict()
    Scheme['Timetable'] = Execute_Plan
    Scheme['Configurations'] = configurations

    with open(project_path + '/Schemes/Daily_Schemes/' +
                      name + '.' + type, 'w') as outfile:
        json.dump(Scheme, outfile)


def gen_Scheme(name):
    dailyConfigs = DailyConfigReader()
    Scheme_Type, Other_Params = dailyConfigs.getScheme_Settings()
    time_Table, type_Table = dailyConfigs.getDaily_Scheme()
    configurations = dailyConfigs.getConfigurations()

    if Scheme_Type == 'Pomodoro':
        Execute_Plan = pomo_Gen_Execute_Plan(
            types_To_Apply_Pomo,  # Global Variable
            time_Table, type_Table,
            Other_Params, pomo_Modes)

    scheme_Writter(name, Scheme_Type, Execute_Plan, configurations)


##
if __name__ == '__main__':
    from pprint import pprint

    name = 'test_PomoScheme1'
    gen_Scheme(name)
    with open(project_path + '/Schemes/Daily_Schemes/test_PomoScheme1.Pomodoro') as Scheme:
        pprint(json.load(Scheme))
