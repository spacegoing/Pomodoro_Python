from datetime import datetime
import time
from threading import Thread, Lock

lock = Lock()


class Alarm():
    def __init__(self, Behavior):
        '''

        :param Behavior: instance of implementation of class Behavior
        :return:
        '''
        self.Behavior = Behavior
        self.lock = lock

    def timer(self, seconds=0, end_datetime=0):
        '''
        Only accept 1 argument, must be explicitly declared
        Either sleep seconds Or sleep until end_datetime.
        :param seconds: int
        :param end_datetime: datetime.time
        :return:
        '''
        self.Behavior.enter_behavior()

        if seconds != 0:
            for i in range(seconds):
                time.sleep(0.9999)  # This is to let TimerController easily acquire the lock
                with self.lock:
                    self.Behavior.in_timer_behavior()
                    time.sleep(0.0001)
        else:
            while datetime.now().time() < end_datetime:
                time.sleep(0.9999)  # This is to let TimerController easily acquire the lock
                with self.lock:
                    self.Behavior.in_timer_behavior()
                    time.sleep(0.0001)

        self.Behavior.exit_behavior()


class AlarmController(Thread):
    '''
    This class should be passed to KeyboardListener under current implementation.
    It will be refractored to Pomo_Alarm in the future.
    '''
    def __init__(self):
        super().__init__()
        self.lock = lock

    def pause(self):
        '''
        pause doesn't work for the case end_datetime is passed in.
        Cause it use datetime.now().time() to calculate remaining time.
        To pause this, it's required to recalculate the Scheme when
        user resume the alarm.
        :return:
        '''
        self.lock.acquire()

    def resume(self):
        self.lock.release()


class Behavior(object):
    '''
    Interface.

    All following methods should be implemented.
    '''

    def __init__(self):
        pass

    def enter_behavior(self):
        pass

    def in_timer_behavior(self):
        pass

    def exit_behavior(self):
        pass


if __name__ == '__main__':
    pass
