from Pomo_Daily_Alarm import pomo_Alarm
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
rawSchema = [["9:00", work],
             ["12:00", relax],
             ["14:00", work],
             ["18:30", relax],
             ["19:30", work],
             ["22:30", sleep]]

Scheme_Type = "Pomodoro"
pomoParams = dict()
pomoParams['pomo_Work_Time'] = 30
pomoParams['pomo_Short_Break'] = 5
# Every pomoLongRelaxPeriod have a long break
pomoParams['pomo_Long_Break_Period'] = 4
pomoParams['pomo_Long_Break'] = 10
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

