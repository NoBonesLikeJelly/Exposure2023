import os
import subprocess
import threading
import pygame
import socket
import time
from pygame.locals import *


SOCKPATH = "/var/run/lirc/lircd"

sock = None

# Define your video directory and list of video files
video_directory = "/mnt/usbdrive0/"
#video_directory = "./TestExposureRaspi/TestVideos/"

selected_index = 0

def get_menu_items(video_directory):
    menu_items = []
    for filename in os.listdir(video_directory):
        if filename.lower().endswith(".mp4") or filename.lower().endswith(".mov") and  os.path.isfile(os.path.join(video_directory, filename)):
            #image_filename = os.path.splitext(filename)[0] + ".png"
            menu_items.append((filename,f"Play {os.path.splitext(filename)[0]}"))
    return menu_items


video_files = get_menu_items(video_directory)

video_playing = False

ir_selected = False

IR_Event = None
IR_Event_Type = None
IR_Event_Data = None

screen = None
font = None

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

SCREEN_WIDTH = None
SCREEN_HEIGHT = None

# Initialize VLC subprocess
vlc_player = None



def load_menu():
    global screen, font, SCREEN_WIDTH, SCREEN_HEIGHT, IR_Event, IR_Event_Type
    # Pygame initialization
    pygame.init()
    pygame.display.set_caption("Video Player Menu")

    monitor_info = pygame.display.Info()

    SCREEN_WIDTH = monitor_info.current_w
    SCREEN_HEIGHT = monitor_info.current_h

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    font = pygame.font.Font(None, 36)
    pygame.mouse.set_visible(False)

    IR_Event_Type = pygame.USEREVENT + 1
    IR_Event = pygame.event.Event(IR_Event_Type, message="IR Event Triggered",data=IR_Event_Data)

    return screen, font

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
    print("Data")
    print(words)

    return words[2], words[1]

def play_video(video_file):
    global vlc_player, video_playing
    if vlc_player is not None:
        vlc_player.terminate()
    video_playing = True
    #vlc_command = f"sudo -u twilliams /Applications/VLC.app/Contents/MacOS/VLC '{video_file}' --no-repeat --play-and-exit --fullscreen"  # Replace with the appropriate VLC command
    vlc_command = f"cvlc '{video_file}' --no-repeat --play-and-exit --fullscreen --no-video-title-show"  # Replace with the appropriate VLC command
    vlc_player = subprocess.Popen(vlc_command, shell=True)
    time.sleep(3)
    pygame.quit()
    vlc_player.wait()
    video_playing = False
    load_menu()
    time.sleep(1)



def input_listener():
    global selected_index, vlc_player, ir_selected, video_playing, IR_Event, IR_Event_Data
    while True:
        keyname, updown = next_key()
        if keyname.decode('utf-8') == "KEY_DOWN" and updown.decode('utf-8') == "00":
            IR_Event.data = "Down"
            pygame.event.post(IR_Event)
        elif keyname.decode('utf-8') == "KEY_UP" and updown.decode('utf-8') == "00":
            IR_Event.data = "Up"
            pygame.event.post(IR_Event)
        elif keyname.decode('utf-8') == "KEY_OK" and updown.decode('utf-8') == "00":
            IR_Event.data = "Enter"
            pygame.event.post(IR_Event)
        elif keyname.decode('utf-8') == "KEY_BACK" and updown.decode('utf-8') == "00":
            pygame.quit()
        print(keyname.decode('utf-8'))


# Main menu loop

if __name__ == "__main__":

    init_irw()

    input_thread = threading.Thread(target=input_listener)
    input_thread.daemon = True
    input_thread.start()

    load_menu()

    running = True
    while running:
        while not video_playing:
            screen.fill(BLACK)
            for i, (video_file, video_name) in enumerate(video_files):
                text = font.render(video_name, True, RED if i == selected_index else WHITE)
                text_rect = text.get_rect()
                text_rect.center = (SCREEN_WIDTH // 2, 50 + i * 40)  # Center horizontally, maintain vertical position
                screen.blit(text, text_rect)

            pygame.display.flip()

            '''
            if ir_selected:
                ir_selected = False
                selected_video = os.path.join(video_directory, video_files[selected_index][0])
                play_video(selected_video)
            '''
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == IR_Event_Type:
                    custom_data = event.data
                    print("Event triggerereed")
                    if custom_data == "Enter":
                        selected_video = os.path.join(video_directory, video_files[selected_index][0])
                        play_video(selected_video)
                    elif custom_data == "Up":
                        selected_index = (selected_index - 1) % len(video_files)
                    elif custom_data == "Down":
                        selected_index = (selected_index + 1) % len(video_files)
                    elif custom_data == "Exit":
                        pygame.quit()
                elif event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        selected_index = (selected_index + 1) % len(video_files)
                    elif event.key == K_UP:
                        selected_index = (selected_index - 1) % len(video_files)
                    elif event.key == K_RETURN:
                        selected_video = os.path.join(video_directory, video_files[selected_index][0])
                    elif event.key == K_ESCAPE:
                        pygame.quit()

    # Clean up when done
    if vlc_player is not None:
        vlc_player.terminate()

    pygame.quit()