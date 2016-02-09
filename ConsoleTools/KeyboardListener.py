# -*- coding: utf-8 -*-
__author__ = 'spacegoing'
##
from threading import Thread
import selectors, sys, os

# Below are all global variables
file_path = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.abspath(os.path.join(file_path, os.path.pardir))
with open(project_path+"/Config/shortcuts_list.org", 'r') as infile:
    shortcuts_list = infile.readlines()
shortlist_len = len(shortcuts_list)


class LSTN_IO:
    printed_lines_no = 1
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    Remove_LINE = ERASE_LINE + CURSOR_UP_ONE

    # def init_command_input(self):
    #     print('Type "p" to display all supported commands', flush=True)
    #     print('Enter pomo commands here: ', end='', flush=True)
    #     self.printed_lines_no += 2

    def incr_lines_no(self):
        self.printed_lines_no += 1

    def print(self, string, end='\n', flush=False):
        print(string, end=end, flush=flush)
        self.printed_lines_no += 1

    def clear_screen(self):
        print(self.Remove_LINE * self.printed_lines_no)
        self.printed_lines_no = 1

    def remove_lines(self, lines_no):
        if self.printed_lines_no > 1:
            for i in range(lines_no):
                print(self.Remove_LINE, flush=True)
            self.printed_lines_no -= lines_no

    def disp_printed_lines(self):
        print(str(self.printed_lines_no))
        self.printed_lines_no += 1


class KbdListener(Thread):
    lstnio = LSTN_IO()

    def __init__(self, TimerController):
        super().__init__()
        self.controller = TimerController()

    def shortcut_callbacks(self, stdin, mask):
        if sys.stdin == stdin:
            self.lstnio.incr_lines_no()
            input_chars = stdin.readline().strip()

            if input_chars == 'l':
                for s in shortcuts_list:
                    self.lstnio.print(s, end='', flush=True)

            if input_chars == 'g':
                self.lstnio.clear_screen()
                # self.lstnio.init_command_input()

            if input_chars == 'd':
                self.lstnio.disp_printed_lines()

            if input_chars == 'r':
                self.controller.resume()

            if input_chars == 'p':
                self.controller.pause()

    def run(self):
        sel = selectors.DefaultSelector()
        sel.register(sys.stdin, selectors.EVENT_READ, self.shortcut_callbacks)

        # self.lstnio.init_command_input()
        while True:
            events = sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)


if __name__ == '__main__':
    from Alarms.Alarm import AlarmController

    listner = KbdListener(AlarmController)
