# The following should be in Stats Module

from datetime import datetime, date, timedelta
from dateutil.parser import parse as timeParser
import os
import json
from pprint import pprint

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


def read_Scheme_JSON(name, mode_Type):
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

    return execute_Timetable, execute_Modetable


def subtract_Time_Objects(start, end):
    """
    Important: start, end should be in one day.

    :param start: datetime.time object.
    :param end: datetime.time object.
    :return:
    """
    time_Diff = datetime.combine(date.today(), end) - \
                datetime.combine(date.today(), start)

    return time_Diff


def comp_Scheme_Stats(execute_Timetable, execute_Modetable):
    """

    :param execute_Timetable: 2D List of datetime.time object
    :param execute_Modetable: List of mode strings.
    :return:
    total_Timedelta: timedelta
    """

    total_Timedelta = timedelta(seconds=0)
    total_Pomos = 0
    for t, m in zip(execute_Timetable, execute_Modetable):
        if m in work_Mode:
            total_Timedelta += subtract_Time_Objects(t[0], t[1])
            total_Pomos += 1

    return total_Timedelta, total_Pomos


def display_Total_Working_Hours(total_Timedelta):
    hours = total_Timedelta.seconds / 3600
    print("Total Working time: " + str(hours))


def display_Total_Pomos(total_Pomos):
    print("Total Pomos a day: " + str(total_Pomos))


def show_Pomo_Stats(name, mode_Type):
    execute_Timetable, execute_Modetable = read_Scheme_JSON(name, mode_Type)
    total_Timedelta, total_Pomos = comp_Scheme_Stats(execute_Timetable, execute_Modetable)
    display_Total_Pomos(total_Pomos)
    display_Total_Working_Hours(total_Timedelta)
