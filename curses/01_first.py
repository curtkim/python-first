import curses

def do_in_body(stdscr):
    ### body
    stdscr.clear()
    # This raises ZeroDivisionError when i == 10.
    for i in range(0, 10):
        v = i - 10
        stdscr.addstr(i, 0, '10 divided by {} is {}'.format(v, 10 / v))

    stdscr.refresh()
    stdscr.getkey()


stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

do_in_body(stdscr)

curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
