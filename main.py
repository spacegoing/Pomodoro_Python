from Pomo_Alarm import pomo_Alarm
from generateSchemeFuncs import gen_Scheme
from writeConfigFuncs import createScehma, createConfigJSON
from StatMining.DailySchemeStats import show_Pomo_Stats

## Create SchemeR
name = 'Home_Pomo_Scheme'

# Create Config File
work = "Work"
relax = "Relax"
sleep = "Sleep"
isContinu = True
rawSchema = [["8:10", work],
             ["12:00", relax],
             ["14:30", work],
             ["19:00", relax],
             ["20:30", work],
             ["22:30", sleep]]

Scheme_Type = "Pomodoro"
pomoParams = dict()
pomoParams['pomo_Work_Time'] = 40
pomoParams['pomo_Short_Break'] = 8
# Every pomoLongRelaxPeriod have a long break
pomoParams['pomo_Long_Break_Period'] = 3
pomoParams['pomo_Long_Break'] = 15
Scheme_Settings = {"Scheme_Type": Scheme_Type,  # Must Have
                   "Pomo_Params": pomoParams  # Only for Pomodoro
                   }

# The following 2 methods should be merged.
DailyScheme = createScehma(rawSchema, isContinu)
createConfigJSON(DailyScheme,
                 Scheme_Settings,
                 None)

# Create Execute_Plan
gen_Scheme(name)

## Activate Alarm
if __name__ == '__main__':
    mode_Type = 'Pomodoro'
    is_Dynamic_Scheme = True
    show_Pomo_Stats(name, mode_Type)
    pomo_Alarm(name, mode_Type, is_Dynamic_Scheme)

