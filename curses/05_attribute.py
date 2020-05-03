import curses
from curses import wrapper

def main(stdscr):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)

    # Clear screen
    stdscr.clear()
    stdscr.addstr(0, 0, "Current mode: Typing mode", curses.A_REVERSE)
    stdscr.refresh()
    stdscr.getkey()

    stdscr.clear()
    stdscr.addstr("Pretty text", curses.color_pair(1))
    stdscr.refresh()
    stdscr.getkey()

wrapper(main)

print(f"curses.can_change_color() = {curses.can_change_color()}")