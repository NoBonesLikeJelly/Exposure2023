import os
import subprocess
import threading
import pygame
import time
from pygame.locals import *

# Define your video directory and list of video files
video_directory = "/mnt/usbdrive0/"
#video_directory = "./TestExposureRaspi/TestVideos/"

def get_menu_items(video_directory):
    menu_items = []
    for filename in os.listdir(video_directory):
        if filename.lower().endswith(".mp4") or filename.lower().endswith(".mov") and  os.path.isfile(os.path.join(video_directory, filename)):
            #image_filename = os.path.splitext(filename)[0] + ".png"
            menu_items.append((filename))
    return menu_items

video_files = get_menu_items(video_directory)

video_playing = False

screen = None
font = None

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialize VLC subprocess
vlc_player = None


def load_menu():
    global screen, font
    # Pygame initialization
    pygame.init()
    pygame.display.set_caption("Video Player Menu")

    monitor_info = pygame.display.Info()

    SCREEN_WIDTH = monitor_info.current_w
    SCREEN_HEIGHT = monitor_info.current_h

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(None, 36)
    return screen, font

def play_video(video_file):
    global vlc_player, video_playing
    if vlc_player is not None:
        vlc_player.terminate()
    video_playing = True
    pygame.quit()
    #vlc_command = f"sudo -u twilliams /Applications/VLC.app/Contents/MacOS/VLC '{video_file}' --no-repeat --play-and-exit --fullscreen"  # Replace with the appropriate VLC command
    vlc_command = f"cvlc '{video_file}' --no-repeat --play-and-exit --fullscreen"  # Replace with the appropriate VLC command
    vlc_player = subprocess.Popen(vlc_command, shell=True)
    vlc_player.wait()
    load_menu()
    video_playing = False



def input_listener():
    
    time.sleep(5)
    selected_video = os.path.join(video_directory, video_files[selected_index])
    play_video(selected_video)


selected_index = 0

# Main menu loop

if __name__ == "__main__":


    input_thread = threading.Thread(target=input_listener)
    input_thread.daemon = True
    input_thread.start()

    load_menu()

    running = True
    while running:
        while not video_playing:
            screen.fill(BLACK)
            for i, video_file in enumerate(video_files):
                text = font.render(video_file, True, RED if i == selected_index else WHITE)
                screen.blit(text, (50, 50 + i * 40))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        selected_index = (selected_index + 1) % len(video_files)
                    elif event.key == K_UP:
                        selected_index = (selected_index - 1) % len(video_files)
                    elif event.key == K_RETURN:
                        selected_video = os.path.join(video_directory, video_files[selected_index])
                        play_video(selected_video)
                    elif event.key == K_ESCAPE:
                        pygame.quit()

    # Clean up when done
    if vlc_player is not None:
        vlc_player.terminate()

    pygame.quit()
