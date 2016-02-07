from datetime import datetime
import time


class Alarm(object):
    def __init__(self, Behavior):
        '''

        :param Behavior: instance of implementation of class Behavior
        :return:
        '''
        self.Behavior = Behavior

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
                time.sleep(1)
                self.Behavior.in_timer_behavior()
        else:
            while datetime.now().time() < end_datetime:
                time.sleep(1)
                self.Behavior.in_timer_behavior()

        self.Behavior.exit_behavior()

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
