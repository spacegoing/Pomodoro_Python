##

import time
import os
from Alarms.Alarm import Alarm, Behavior, AlarmController
from ConsoleTools.KeyboardListener import KbdListener
from itertools import cycle

# Todo: Same as generateSchemeFuncs, should be changed to mode params
short_Break_Mode = 'pomo_Short_Break_Mode'
long_Break_Mode = 'pomo_Long_Break_Mode'
work_Mode = 'pomo_Work_Mode'
stop_Mode = 'pomo_Stop_Mode'
pomo_Modes = [short_Break_Mode, long_Break_Mode, work_Mode, stop_Mode]
Break_Modes = [long_Break_Mode, short_Break_Mode]
Work_Modes = [work_Mode]
Work_Sound = "/Users/hhxjzyr/Music/网易云音乐/Alan Silvestri - Forrest Gump Suite.mp3"
Break_Sound = "/Users/hhxjzyr/Music/网易云音乐/Evanescence - My Immortal.mp3"

pomoParams = dict()
pomoParams['pomo_Work_Time'] = 45
pomoParams['pomo_Short_Break'] = 10
# Every pomoLongRelaxPeriod have a long break
pomoParams['pomo_Long_Break_Period'] = 2
pomoParams['pomo_Long_Break'] = 20

class Pomodoro_One_Behavior(Behavior):
    def __init__(self,seconds,mode):

        """
        :param seconds int
        :param mode string
        :return
        """

        super().__init__()
        # these subClass(Pomodoro_One_Behavior)'s attributes value all come from global variables defined above
        self.work_Mode = work_Mode
        self.short_Break_Mode  = short_Break_Mode
        self.long_Break_Mode = long_Break_Mode
        self.Break_Modes=[self.long_Break_Mode, self.short_Break_Mode]
        self.Work_Modes = [self.work_Mode]
        self.Work_Sound = Work_Sound
        self.Break_Sound = Break_Sound
        # these attributes value come from __init__'s parameter
        self.time_Remaining=seconds
        self.curr_mode = mode

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
        print("Current Mode: %s"
              % (self.curr_mode), flush=True)
        self.alarm_Actions()

    def in_timer_behavior(self):
        self.time_Remaining-=1
        timeShow=time.strftime('%H:%M:%S', time.gmtime(self.time_Remaining))
        print('\rTime Remaining: %s' % timeShow,end='', flush=True)

    def exit_behavior(self):
        print('\r', end='', flush=True)




def pomo_one_genScheme(pomoParams):
    """

    :param pomoParams: a dictionary
    :return:
    secondsTable is a generator, a infinite repeating of  ['work','short_break,work,long_break,work,long_break],depending
    on your pomo_Long_Break_Period.
    modeTable is a generator, a infinite repeating of [work_time,short_break_time,work_time,long_break_time],depending
    on your pomo_Long_Break_Period.
    """

    pomo_Mode_Vector = [work_Mode, short_Break_Mode] * pomoParams['pomo_Long_Break_Period']
    pomo_Mode_Vector[-1] = long_Break_Mode

    pomo_Time_Vector = [pomoParams['pomo_Work_Time']*60, pomoParams['pomo_Short_Break']*60] * pomoParams['pomo_Long_Break_Period']
    pomo_Time_Vector[-1] = pomoParams['pomo_Long_Break']*60

    secondsTable=cycle(pomo_Time_Vector)
    modeTable=cycle(pomo_Mode_Vector)

    return secondsTable,modeTable


def pomo_one_Alarm(pomoParams):
    secondsTable,modeTable= pomo_one_genScheme(pomoParams)
    kbd_lstn = KbdListener(AlarmController)
    kbd_lstn.start()

    # Never stop unless user terminate it in console
    for seconds,mode in zip(secondsTable,modeTable):
        one_pomo_alarm = Pomodoro_One_Behavior(seconds=seconds,mode=mode)
        one_pomo = Alarm(one_pomo_alarm)
        one_pomo.timer(seconds)


##
if __name__=='__main__':
    pomo_one_Alarm(pomoParams=pomoParams)