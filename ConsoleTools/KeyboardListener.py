# -*- coding: utf-8 -*-
__author__ = 'spacegoing'
##
import selectors
import sys

with open("../Config/shortcuts_list.txt", 'r') as infile:
    shortcuts_list = infile.readlines()
shortlist_len = len(shortcuts_list)

aaa = []
lines_no = 25
for i in range(lines_no):
    aaa.append('line no: %d\n' % i)


class LSTN_IO:
    printed_lines_no = 0
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    Remove_LINE = ERASE_LINE + CURSOR_UP_ONE

    def incr_lines_no(self):
        self.printed_lines_no += 1

    def print(self, string, end='\n', flush='False'):
        print(string, end=end, flush=flush)
        self.printed_lines_no += 1

    def clear_screen(self):
        print(self.Remove_LINE * self.printed_lines_no)
        self.printed_lines_no = 0

    def remove_lines(self, lines_no):
        for i in range(lines_no):
            print(self.Remove_LINE, flush=True)
        self.printed_lines_no -= lines_no

    def init_command_input(self):
        print('Type "p" to display all supported commands', flush=True)
        print('Enter pomo commands here: ', end='', flush=True)
        self.printed_lines_no += 2

    def disp_printed_lines(self):
        print(str(self.printed_lines_no))
        self.printed_lines_no += 1


lstnio = LSTN_IO()


def printShortcuts(stdin, mask):
    if sys.stdin == stdin:
        lstnio.incr_lines_no()
        input_chars = stdin.readline().strip()

        if input_chars == 'p':
            for s in shortcuts_list:
                lstnio.print(s, end='', flush=True)

        if input_chars == 'g':
            lstnio.clear_screen()
            lstnio.init_command_input()

        if input_chars == 'a':
            lstnio.disp_printed_lines()


def main():
    sel = selectors.DefaultSelector()
    sel.register(sys.stdin, selectors.EVENT_READ, printShortcuts)

    lstnio.init_command_input()
    while True:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)


if __name__ == '__main__':
    main()
