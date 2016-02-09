# -*- coding: utf-8 -*-
__author__ = 'spacegoing'
from dateutil.parser import parse as timeParser
from datetime import timedelta, datetime
import json, os

# Below are all global variables
file_path = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.abspath(os.path.join(file_path, os.path.pardir))
# Todo: Same as generateSchemeFuncs, should be changed to mode params
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


def pomo_Daily_Scheme_Algo(start, end,
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
            start = timeParser(start)
            end = timeParser(end)

            execute_Plan = pomo_Daily_Scheme_Algo(start, end, *pomo_Modes, **pomo_Params)
            # Loop: Reformat Execute Plan to [Start, End, Mode] format.
            lenPlan = len(execute_Plan)
            for i in range(lenPlan - 1):
                pomo_Execute_Plan.append([str(execute_Plan[i][0].time()),  # Start time
                                          str(execute_Plan[i + 1][0].time()),  # End time
                                          str(execute_Plan[i][1])])  # Mode
        else:
            pomo_Execute_Plan.append([start, end, t])

    return pomo_Execute_Plan


def replace_deprecated_Pomo_Period(execute_Plan,
                                   pomo_start_at_period,
                                   pomo_end_at_period,
                                   execute_Timetable,
                                   execute_Modetable):
    """
    Update execute_Timetable, execute_Modetable with new computed
    ones. Don't need to return cause List is in place modified.
    :param execute_Plan:
    :param pomo_start_at_period:
    :param pomo_end_at_period:
    :param execute_Timetable:
    :param execute_Modetable:
    :return:
    """
    new_Pomo_Timetable = list()
    new_Pomo_Modetable = list()
    lenPlan = len(execute_Plan)
    for i in range(lenPlan - 1):
        new_Pomo_Timetable.append([execute_Plan[i][0].time(),  # Start time
                                   execute_Plan[i + 1][0].time()  # End time
                                   ])
        new_Pomo_Modetable.append(execute_Plan[i][1])

    execute_Timetable[:] = execute_Timetable[:pomo_start_at_period] \
                           + new_Pomo_Timetable \
                           + execute_Timetable[pomo_end_at_period:]
    execute_Modetable[:] = execute_Modetable[:pomo_start_at_period] \
                           + new_Pomo_Modetable \
                           + execute_Modetable[pomo_end_at_period:]


def dynamic_Pomo_Scheme(execute_Timetable, execute_Modetable,
                        pomo_Modes, pomo_Params):
    """
    According to Current_Time. Search the whole Pomo Period (all Pomo_Modes)
    the current time in. The recalculate the period use the current time
    as start point.
    Original Scheme (the one stored in JSON file) will be replaced.

    Todo: should save changes in the JSON file again.

    :param execute_Modetable:
    :param execute_Timetable:
    :return:
    In_place modify Modetable and Timetable. No return.
    """
    current_Time = datetime.now().time()

    len_Scheme = len(execute_Timetable)
    for period_index in range(len_Scheme):
        period_end_time = execute_Timetable[period_index][1]

        if current_Time <= period_end_time:
            if execute_Modetable[period_index] in pomo_Modes:

                # Find continuous Pomo Modes start-end time
                for i in range(period_index, len_Scheme):
                    if execute_Modetable[i] not in pomo_Modes:
                        end_time = execute_Timetable[i][0]  # Start time of this period
                        pomo_end_at_period = i

                        # Recalculate Pomo timetable
                        # end_time now is datetime.time() object
                        # argument of pomo_Daily_Scheme_Algo require datetime.datetime() object
                        end_time = timeParser(str(end_time))
                        start_time = timeParser(str(current_Time))

                        execute_Plan = pomo_Daily_Scheme_Algo(start_time, end_time,
                                                              *pomo_Modes, **pomo_Params)

                        # replace previous Pomo Modes Period
                        replace_deprecated_Pomo_Period(execute_Plan,
                                                       period_index,
                                                       pomo_end_at_period,
                                                       execute_Timetable,
                                                       execute_Modetable)
                        break
                break


# Todo: Need to save dynamic history for daily stat record
def read_Scheme_JSON(name, mode_Type, is_Dynamic_Scheme):
    """

    :param name:
    :param mode_Type:
    :return:
    execute_Timetable: 2D List of datetime.time object
    execute_Modetable: List of mode strings.
    """
    with open(project_path + "/Schemes/Daily_Schemes/" + name + "." + mode_Type) as openFile:
        Scheme = json.load(openFile)
    execute_Timetable = [[timeParser(i).time() for i in j[:-1]]
                         for j in Scheme['Timetable']]
    execute_Modetable = [i[-1] for i in Scheme['Timetable']]

    if is_Dynamic_Scheme:
        scheme_Params = Scheme['Configurations']['Scheme_Settings']['Pomo_Params']
        dynamic_Pomo_Scheme(execute_Timetable, execute_Modetable,
                            pomo_Modes, scheme_Params)

    return execute_Timetable, execute_Modetable
