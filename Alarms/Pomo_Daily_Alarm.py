##
import os
from datetime import datetime
from Alarms.Alarm import Alarm, Behavior, AlarmController
from ConsoleTools.KeyboardListener import KbdListener
from dateutil.parser import parse as timeParser
from Pomo_Scheme import read_Scheme_JSON

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


class Pomo_Alarm_Behavior(Behavior):
    # TODO: should be written into config file
    def __init__(self, start_time, end_time, mode):
        '''

        :param start_time: datetime.time()
        :param end_time: datetime.time()
        :param mode: string. mode string.
        :return:
        '''
        super().__init__()
        self.short_Break_Mode = 'pomo_Short_Break_Mode'
        self.long_Break_Mode = 'pomo_Long_Break_Mode'
        self.work_Mode = 'pomo_Work_Mode'
        self.Break_Modes = [self.long_Break_Mode, self.short_Break_Mode]
        self.Work_Modes = [self.work_Mode]
        self.Work_Sound = "/Users/spacegoing/Music/网易云音乐/Emma Stevens - A Place Called You.mp3"
        self.Break_Sound = "/Users/spacegoing/Music/网易云音乐/Emily Grace - Mr Parker.mp3"

        self.start_time = start_time
        self.end_time = end_time
        self.curr_mode = mode

    # Todo: if startwith 0 only display MS
    def delta_to_HMS(self, timedelta):
        return str(timedelta).split('.')[0]

    def play_Break_Sound(self):
        os.system("open '" + self.Break_Sound + "'")

    def play_Work_Sound(self):
        os.system("open '" + self.Work_Sound + "'")

    def alarm_Actions(self):
        if self.curr_mode in self.Break_Modes:
            self.play_Break_Sound()
        elif self.curr_mode in self.Work_Modes:
            self.play_Work_Sound()

    def enter_behavior(self):
        print("Current Mode: %s    From %s to %s"
              % (self.curr_mode,
                 self.delta_to_HMS(self.start_time),
                 self.delta_to_HMS(self.end_time)
                 ), flush=True
              )
        self.alarm_Actions()

    def in_timer_behavior(self):
        """

        :param curr: datetime.datetime object
        :param end: datetime.datetime object
        :return:
        """
        curr = datetime.now().time()
        time_Remaining = timeParser(str(self.end_time)) - timeParser(str(curr))
        print('\rTime Remaining: %s' % str(time_Remaining).split('.')[0], end='', flush=True)

    def exit_behavior(self):
        print('\r', end='', flush=True)


def pomo_Alarm(name, mode_Type, is_Dynamic_Scheme):
    execute_Timetable, execute_Modetable \
        = read_Scheme_JSON(name, mode_Type, is_Dynamic_Scheme)

    currentTime = datetime.now().time()
    kbd_lstn = KbdListener(AlarmController)
    kbd_lstn.start()

    # Stop when the day (timetable) end.
    for start_end_period, mode in zip(execute_Timetable, execute_Modetable):
        if currentTime <= start_end_period[1]:
            pomo_alarm = Pomo_Alarm_Behavior(start_end_period[0], start_end_period[1], mode)
            alarm = Alarm(pomo_alarm)
            alarm.timer(end_datetime=start_end_period[1])


##
if __name__ == '__main__':
    name = 'Home_Pomo_Scheme'
    mode_Type = 'Pomodoro'
    is_Dynamic_Scheme = True
    pomo_Alarm(name, mode_Type, is_Dynamic_Scheme)
