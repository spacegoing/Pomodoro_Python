import time
from dateutil.parser import parse as timeParser

def show_Remaining_Time(curr,end):
    """

    :param curr: datetime.datetime object
    :param end: datetime.datetime object
    :return:
    """
    time_Remaining = timeParser(str(end)) - timeParser(str(curr))
    print('\rTime Remaining: %s' % str(time_Remaining).split('.')[0], end ='', flush=True)

if __name__ == '__main__':
    import datetime
    end = '14:59:59'
    while True:
        curr = datetime.datetime.now().time()
        show_Remaining_Time(curr,end)
        time.sleep(1)

