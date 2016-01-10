##
from dateutil.parser import parse as timeParser
from datetime import datetime
import time
import os
import json
from pprint import pprint

# Todo: Bad design. Functional Coupling with another module?
from generateSchemeFuncs import pomo_Algo
from Alarm.Alarm import show_Remaining_Time

# Below are all global variables
file_path = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.abspath(os.path.join(file_path, os.path.pardir))

# Todo: Same as generateSchemeFuncs, should be changed to mode params
short_Break_Mode = 'pomo_Short_Break_Mode'
long_Break_Mode = 'pomo_Long_Break_Mode'
work_Mode = 'pomo_Work_Mode'
stop_Mode = 'pomo_Stop_Mode'
pomo_Modes = [short_Break_Mode, long_Break_Mode, work_Mode, stop_Mode]
Break_Modes = [long_Break_Mode, short_Break_Mode]
Work_Modes = [work_Mode]
Work_Sound = "/Users/spacegoing/Music/网易云音乐/Emma Stevens - A Place Called You.mp3"
Break_Sound = "/Users/spacegoing/Music/网易云音乐/Emily Grace - Mr Parker.mp3"

# Todo: if startwith 0 only display MS
def delta_to_HMS(timedelta):
    return str(timedelta).split('.')[0]


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
    for pomo_start_at_period in range(len_Scheme):
        period_end_time = execute_Timetable[pomo_start_at_period][1]

        if current_Time <= period_end_time:
            if execute_Modetable[pomo_start_at_period] in pomo_Modes:

                # Find continuous Pomo Modes start-end time
                for i in range(pomo_start_at_period, len_Scheme):
                    if execute_Modetable[i] not in pomo_Modes:
                        end_time = execute_Timetable[i][0]  # Start time of this period
                        pomo_end_at_period = i

                        # Recalculate Pomo timetable
                        # end_time now is datetime.time() object
                        # argument of pomo_Algo require datetime.datetime() object
                        end_time = timeParser(str(end_time))
                        start_time = timeParser(str(current_Time))

                        execute_Plan = pomo_Algo(start_time, end_time,
                                                 *pomo_Modes, **pomo_Params)

                        # replace previous Pomo Modes Period
                        replace_deprecated_Pomo_Period(execute_Plan,
                                                       pomo_start_at_period,
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


def play_Break_Sound(Break_Sound):
    os.system("open '" + Break_Sound + "'")


def play_Work_Sound(Work_Sound):
    os.system("open '" + Work_Sound + "'")


def alarm_Actions(mode):
    if mode in Break_Modes:
        play_Break_Sound(Break_Sound)
    elif mode in Work_Modes:
        play_Work_Sound(Work_Sound)


def pomo_Alarm(name, mode_Type, is_Dynamic_Scheme):
    execute_Timetable, execute_Modetable \
        = read_Scheme_JSON(name, mode_Type, is_Dynamic_Scheme)

    currentTime = datetime.now().time()
    # Stop when the day (timetable) end.
    for start_end_period, mode in zip(execute_Timetable, execute_Modetable):
        if currentTime <= start_end_period[1]:
            alarm_Actions(mode)  # activate the current mode
            print("Current Mode: %s    From %s to %s"
                  % (mode,
                     delta_to_HMS(start_end_period[0]),
                     delta_to_HMS(start_end_period[1])
                     ), flush=True
                  )
            while True:
                time.sleep(1)
                currentTime = datetime.now().time()

                show_Remaining_Time(currentTime, start_end_period[1])
                if currentTime >= start_end_period[1]:  # If the current mode timeout
                    print('\r', end='', flush=True)  # Cleaning Remaining Time
                    break  # Jump to the next time period


##
if __name__ == '__main__':
    name = 'Home_Pomo_Scheme'
    mode_Type = 'Pomodoro'
    is_Dynamic_Scheme = True
    pomo_Alarm(name, mode_Type, is_Dynamic_Scheme)
