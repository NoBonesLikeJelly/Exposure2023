import curses
import os


def get_menu_items(folder_path):
    menu_items = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".py"") and os.path.isfile(os.path.join(folder_path, filename)):
            menu_items.append((f"Play {filename}", filename))
    menu_items.append(("Exit", "Exit"))
    return menu_items

def display_menu(stdscr, selected_row, menu_items):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    for i, (text, _) in enumerate(menu_items):
        x = w // 2 - len(text) // 2
        y = h // 2 - len(menu_items) // 2 + i

        if i == selected_row:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, os.path.splitext(text)[0])
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, os.path.splitext(text)[0])

    stdscr.refresh()

def main(stdscr):
    # Initialize curses
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    selected_row = 0

    folder_path = "./"
    menu_items = get_menu_items(folder_path)


    while True:
        display_menu(stdscr, selected_row, menu_items)
        key = stdscr.getch()

        if key == curses.KEY_UP and selected_row > 0:
            selected_row -= 1
        elif key == curses.KEY_DOWN and selected_row < len(menu_items) - 1:
            selected_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            _, action = menu_items[selected_row]
            if action == "Exit":
                break  # Exit the program
            else:
                # Execute the selected program (replace with your program execution logic)
                stdscr.clear()
                stdscr.addstr(0, 0, f"Launching {action}...")
                stdscr.refresh()
                curses.napms(1000)  # Sleep for 1 second (simulate program execution)

if __name__ == "__main__":
    curses.wrapper(main)