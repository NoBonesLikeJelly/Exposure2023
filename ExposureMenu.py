import os
import pygame
import subprocess
import threading
import time

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

#folder_path = "./TestExposureRaspi/TestVideos/"
folder_path = "/mnt/usbdrive0/TestExposureRaspi/TestVideos/"

# Global variables
selected_video = None
selected_index = 0

# Set font and font size for the menu
font = pygame.font.Font(None, 36)

def display_menu(video_list):
    global selected_video, selected_index

    running = True

    
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = max(0, selected_index - 1)
                elif event.key == pygame.K_DOWN:
                    selected_index = min(len(video_list) - 1, selected_index + 1)
                elif event.key == pygame.K_RETURN:
                    selected_video = video_list[selected_index]
                elif event.key == pygame.K_SPACE:
                    selected_video = video_list[selected_index]
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()   
    

        screen.fill((0, 0, 0))

        # Display video list
        for i, video_name in enumerate(video_list):
            text = font.render(video_name, True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.center = (screen_width // 2, 100 + i * 50)
            screen.blit(text, text_rect)

        # Highlight the selected video
        pygame.draw.rect(screen, (0, 255, 0), (250, 90 + selected_index * 50, 300, 50), 2)

        pygame.display.flip()

    pygame.quit()

# Function to play the selected video using VLC
def play_video(video_file):
    try:
        #vlc_command = f"cvlc '{folder_path}{video_file}' --no-repeat --play-and-exit --fullscreen --no-xlib"
        vlc_command = f"sudo -u pi cvlc '{folder_path}{video_file}' --no-repeat --play-and-exit --fullscreen"  # Replace with the appropriate VLC command
        subprocess.Popen(vlc_command, shell=True)
    except Exception as e:
        print(f"Error running VLC: {e}")

# Keyboard event listener thread
def keyboard_listener():
    global selected_video, selected_index

    #time.sleep(10)
    #selected_index = min(len(video_files) - 1, selected_index + 1)

if __name__ == "__main__":
    video_dir = folder_path
    video_files = [f for f in os.listdir(video_dir) if f.endswith(".mp4")]

    keyboard_thread = threading.Thread(target=keyboard_listener)
    keyboard_thread.daemon = True  # Make the thread a daemon so it terminates when the main program ends
    keyboard_thread.start()

    while True:
        selected_video = None
        display_menu(video_files)

        if selected_video:
            video_path = os.path.join(video_dir, selected_video)
            play_video(video_path)