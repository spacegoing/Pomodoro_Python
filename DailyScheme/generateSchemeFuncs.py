__author__ = 'spacegoing'
##
from DailyScheme.readConfigFuncs import DailyConfigReader
from dateutil.parser import parse as parseTime
from datetime import timedelta
import json
import os

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


def minutes_To_Timedelta(mins):
    """

    :param mins: int.
    :return: timedelta object
    """
    return timedelta(minutes=mins)


def pomo_Algo(start, end,
              short_Break_Mode, long_Break_Mode,
              work_Mode, stop_Mode,
              pomo_Work_Time, pomo_Short_Break,
              pomo_Long_Break, pomo_Long_Break_Period):
    """

    :param start:
    :param end:

    :param short_Break_Mode:
    :param long_Break_Mode:
    :param work_Mode:
    :param stop_Mode:

    :param pomo_Long_Break: int. e.g. 10 mins.
    :param pomo_Long_Break_Period: int. e.g. Every 4 cycle of pomos.
    :param pomo_Short_Break: int. e.g. 5 mins.
    :param pomo_Work_Time: int. How long a work cycle is. e.g. 25 mins.

    :return:
    pomo_Execute_Plan: 2d List of Strings. [[Start, pomo_Mode],...]
    """

    pomo_Mode_Vector = [work_Mode, short_Break_Mode] * pomo_Long_Break_Period
    pomo_Mode_Vector[-1] = long_Break_Mode

    pomo_Time_Vector = [pomo_Work_Time, pomo_Short_Break] * pomo_Long_Break_Period
    pomo_Time_Vector[-1] = pomo_Long_Break
    pomo_Time_Vector = [minutes_To_Timedelta(i) for i in pomo_Time_Vector]

    count = 0
    reset_Count = len(pomo_Time_Vector) - 1
    pomo_Execute_Plan = list()

    while True:
        if start + pomo_Time_Vector[count] < end:
            pomo_Execute_Plan.append([start, pomo_Mode_Vector[count]])
            start += pomo_Time_Vector[count]
            count += 1

            if count > reset_Count:
                count = 0
        else:
            pomo_Execute_Plan.append([start, pomo_Mode_Vector[count]])
            pomo_Execute_Plan.append([end, stop_Mode])
            break

    return pomo_Execute_Plan


def pomo_Gen_Execute_Plan(types_To_Apply_Pomo, time_Table, type_Table, Other_Params, pomo_Modes):
    """

    :param time_Table: 2d List of Strings. %H:%M
                        Must start from 0:00, end at End_Of_Day_Symbol
    :param type_Table: 1d List of Strings.
    :param types_To_Apply_Pomo: 1d List of Strings. Types pomo algo apply on.

    :param Other_Params:
    :param pomo_Modes:
    :return:
    pomo_Execute_Plan: [[start, end, type]...]
    """
    pomo_Params = Other_Params['Pomo_Params']
    pomo_Execute_Plan = list()

    for [start, end], t in zip(time_Table, type_Table):
        if t in types_To_Apply_Pomo:
            start = parseTime(start)
            end = parseTime(end)

            execute_Plan = pomo_Algo(start, end, *pomo_Modes, **pomo_Params)
            # Loop: Reformat Execute Plan to [Start, End, Mode] format.
            lenPlan = len(execute_Plan)
            for i in range(lenPlan - 1):
                pomo_Execute_Plan.append([str(execute_Plan[i][0].time()),  # Start time
                                          str(execute_Plan[i + 1][0].time()),  # End time
                                          str(execute_Plan[i][1])])  # Mode
        else:
            pomo_Execute_Plan.append([start, end, t])

    return pomo_Execute_Plan


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
