import os
import subprocess
import curses
import socket
import threading
import queue 

# Define a queue for IR keypress notifications
ir_queue = queue.Queue()

SOCKPATH = "/var/run/lirc/lircd"

sock = None

def init_irw():
    global sock
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    print ('starting up on %s' % SOCKPATH)
    sock.connect(SOCKPATH)

def next_key():
    '''Get the next key pressed. Return keyname, updown.
    '''
    while True:
        data = sock.recv(128)
        # print("Data: " + data)
        data = data.strip()
        if data:
            break

    words = data.split()
    #print("Data")
    #print(words)

    return words[2], words[1]

def input_listener():
    global selected_index, vlc_player, ir_selected, video_playing, IR_Event, IR_Event_Data
    while True:
        keyname, updown = next_key()
        if keyname.decode('utf-8') == "KEY_DOWN" and updown.decode('utf-8') == "00":
            key = "Down"
            ir_queue.put(key)
        elif keyname.decode('utf-8') == "KEY_UP" and updown.decode('utf-8') == "00":
            key = "Up"
            ir_queue.put(key)
        elif keyname.decode('utf-8') == "KEY_OK" and updown.decode('utf-8') == "00":
            key = "Enter"
            ir_queue.put(key)
        elif keyname.decode('utf-8') == "KEY_BACK" and updown.decode('utf-8') == "00":
            exit()
        #print(keyname.decode('utf-8'))


def get_video_files(folder_path):
    video_files = [f for f in os.listdir(folder_path) if f.endswith(('.mp4', '.avi', '.mkv'))]
    return video_files

def remove_extension(file_name):
    name, _ = os.path.splitext(file_name)
    return name

def display_menu(stdscr, video_files, selected_video_idx):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    center_y, center_x = height // 2, width // 2

    stdscr.addstr(center_y - len(video_files) // 2 - 1, center_x - 15, "Select a film to play:")
    for i, video in enumerate(video_files):
        video_name = remove_extension(video)
        if i == selected_video_idx:
            stdscr.addstr(center_y + i - len(video_files) // 2, center_x - 15, f" > {video_name}")
        else:
            stdscr.addstr(center_y + i - len(video_files) // 2, center_x - 15, f"   {video_name}")
    stdscr.refresh()

def blank_screen():
    # Use xset to blank the screen
    subprocess.run(['xset', 'dpms', 'force', 'off'])

def unblank_screen():
    # Use xset to unblank the screen
    subprocess.run(['xset', 'dpms', 'force', 'on'])


def main(stdscr):
    #folder_path = "./TestExposureRaspi/TestVideos/"
    folder_path = "/mnt/usbdrive0/"
    video_files = get_video_files(folder_path)

    selected_video_idx = 0
    key = 0

    input_thread = threading.Thread(target=input_listener)
    input_thread.daemon = True
    input_thread.start()

    curses.curs_set(0) 
    
    while key != ord('0'):
        display_menu(stdscr, video_files, selected_video_idx)
        key = stdscr.getch()
        if key == curses.KEY_DOWN and selected_video_idx < len(video_files) - 1:
            key = "Down"
            ir_queue.put(key)
            #selected_video_idx += 1
        elif key == curses.KEY_UP and selected_video_idx > 0:
            key = "Up"
            ir_queue.put(key)
            #selected_video_idx -= 1
        elif key == 10:  # Enter key
            if selected_video_idx == len(video_files):
                break
            selected_video = video_files[selected_video_idx]
            video_path = os.path.join(folder_path, selected_video)
            subprocess.run(['cvlc', video_path, '--no-repeat', '--play-and-exit', '--fullscreen', '--no-video-title-show'])

        try:
            #display_menu(stdscr, video_files, selected_video_idx)
            print("Im trying something herhe")
            ir_key = ir_queue.get_nowait()
            print(ir_key)
            # Handle the IR keypress (e.g., perform actions based on the key)
            if ir_key == "Enter":
                if selected_video_idx == len(video_files):
                    break
                selected_video = video_files[selected_video_idx]
                video_path = os.path.join(folder_path, selected_video)
                subprocess.run(['cvlc', video_path, '--no-repeat', '--play-and-exit', '--fullscreen', '--no-video-title-show'])
            elif ir_key == "Down":
                selected_video_idx += 1
            elif ir_key == "Up":
                selected_video_idx -= 1
        except queue.Empty:
            pass


if __name__ == "__main__":
    init_irw()
    curses.wrapper(main)
