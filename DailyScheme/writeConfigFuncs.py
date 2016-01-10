__author__ = 'spacegoing'
##
import json
import os

file_path = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.abspath(os.path.join(file_path, os.path.pardir))

# TODO: Safety Check.

# All the following are gloabal variables
# Default Period Types
work = "Work"
relax = "Relax"
sleep = "Sleep"
Period_Type_Params = {"Type_List": [work, relax, sleep]}

# Default start/end of day Symbols
endOfDay = "23:59:59.999999"  # datetime's resolution of microseconds
startOfDay = "0:00"
StartEnd_Of_Day_Symbols = {"Start_Of_Day_Symbol": startOfDay,
                           "End_Of_Day_Symbol": endOfDay}


def createPeriod(start, end, type):
    period = dict()
    period['start'] = start
    period['end'] = end
    period['type'] = type

    return period


def parseContinuSchema(contSchema):
    """

    :param contSchema:
    :return:
    """
    finalSchema = list()
    lenSchema = len(contSchema)
    for i in range(lenSchema):
        # Parse the first period
        if i == 0:

            startTime = contSchema[0][0]
            endTime = contSchema[1][0]
            periodType = contSchema[0][1]

            # If user defined 0:00-endTime
            # period type is what user defined
            if startTime == startOfDay:
                finalSchema.append(
                        createPeriod(startOfDay, endTime,
                                     periodType)
                )
            # If user didn't define 0:00-startTime
            # period type is default ("Sleep")
            else:
                finalSchema.append(
                        createPeriod(startOfDay, startTime,
                                     sleep)
                )
                finalSchema.append(
                        createPeriod(startTime, endTime,
                                     periodType)
                )

        # Parse the last period
        elif i == lenSchema - 1:
            startTime = contSchema[i][0]
            endTime = endOfDay  # 24:00 60*24=1440
            periodType = contSchema[i][1]
            finalSchema.append(
                    createPeriod(startTime, endTime,
                                 periodType)
            )
        # For the other periods
        else:
            startTime = contSchema[i][0]
            endTime = contSchema[i + 1][0]
            periodType = contSchema[i][1]
            finalSchema.append(
                    createPeriod(startTime, endTime,
                                 periodType)
            )

    return finalSchema


def parseDiscontSchema(disContSchema):
    """
    The input is disContSchema. It has the very
    strict format

    :param disContSchema: Very Strict Format
            period0: start from 0:00
            periodlast: end at endOfDay
    :return:
    """
    return [createPeriod(r[0], r[1], r[2]) for r in disContSchema]


def createScehma(rawSchema, isContinu):
    """
    :param rawSchema:
    :return:
    """
    if len(rawSchema) < 2:
        raise Exception("Wrong Schema Format. May be not enough periods.")

    if isContinu:
        finalSchema = parseContinuSchema(rawSchema)
    else:
        finalSchema = parseDiscontSchema(rawSchema)

    return finalSchema


def createConfigJSON(DailyScheme,
                     Scheme_Settings,
                     MISC=None):
    """

    :param DailyScheme:
    :param Scheme_Settings:
    :param MISC:

    Default Values:
    :Default Period_Type_Params:
    :Default StartEnd_Symbols_Of_Day:

    :return:
    """

    configs = {"Daily_Scheme_Config":
                   {"DailyScheme": DailyScheme,
                    "Period_Type_Params": Period_Type_Params,
                    "StartEnd_Symbols_Of_Day": StartEnd_Of_Day_Symbols,
                    "Scheme_Settings": Scheme_Settings,
                    "MISC": MISC
                    }
               }

    with open(project_path+'/Config/Daily_Scheme_Config.json', 'w') as outfile:
        json.dump(configs, outfile)


##
if __name__ == "__main__":
    isContinu = True
    rawSchema = [["9:00", work],
                 ["11:30", relax],
                 ["14:00", work],
                 ["17:30", relax],
                 ["19:00", work],
                 ["22:30", sleep]]

    Scheme_Type = "Pomodoro"
    pomoParams = dict()
    pomoParams['pomo_Work_Time'] = 40
    pomoParams['pomo_Short_Break'] = 10
    # Every pomoLongRelaxPeriod have a long break
    pomoParams['pomo_Long_Break_Period'] = 4
    pomoParams['pomo_Long_Break'] = 10
    Scheme_Settings = {"Scheme_Type": Scheme_Type,  # Must Have
                       "Pomo_Params": pomoParams  # Only for Pomodoro
                       }

    DailyScheme = createScehma(rawSchema, isContinu)

    createConfigJSON(DailyScheme,
                     Scheme_Settings,
                     None)
