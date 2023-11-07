import pygame
import os
import subprocess
import threading
import keyboard
import time
import multiprocessing


# Initialize pygame
pygame.init()

# Constants
monitor_info = pygame.display.Info()
SCREEN_WIDTH = monitor_info.current_w
SCREEN_HEIGHT = monitor_info.current_h

IMAGE_SIZE = (110, 150)  # Set the desired image size
  # Set the height of each menu item (including padding)

MENU_FONT_SIZE = 36
MENU_ITEM_SPACING = 50
MENU_TEXT_COLOR = (255, 255, 255)
MENU_SELECTED_COLOR = (0, 255, 0)

# Define the number of rows and columns in the grid
GRID_COLUMNS = 3

# Calculate the width and height of each menu item cell
CELL_WIDTH = SCREEN_WIDTH // GRID_COLUMNS
CELL_PADDING = 50
# Initialize the screen
#screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu")

python_script = "test.py"

menu_items = None
menu_images = None
selected_item = 0

#    folder_path = "/mnt/usbdrive0/"
folder_path = "./TestExposureRaspi/TestVideos/"

# Define the menu items and corresponding commands
def get_menu_items(folder_path):
    menu_items = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".mp4") or filename.lower().endswith(".mov") and  os.path.isfile(os.path.join(folder_path, filename)):
            image_filename = os.path.splitext(filename)[0] + ".png"
            menu_items.append((f"Play {os.path.splitext(filename)[0]}", filename, image_filename))
    return menu_items
def get_menu_images(folder_path, menu_items):
    menu_images = {}
    for _, script_filename, image_filename in menu_items:
        image_path = os.path.join(folder_path, image_filename)
        if os.path.exists(image_path):
            print(f"Image Path is: {image_path}")
            try:
                menu_images[image_filename] = pygame.image.load(image_path)
            except pygame.error as e:
                print(f"Error loading image: {e}")
    return menu_images

#def event_listener():

def run_vlc(folder_path, video_file):
    try:
        vlc_command = f"sudo -u twilliams /Applications/VLC.app/Contents/MacOS/VLC '{folder_path}{video_file}' --no-repeat --play-and-exit --fullscreen"  # Replace with the appropriate VLC command
#        vlc_command = f"sudo -u pi cvlc '{folder_path}{video_file}' --no-repeat --play-and-exit --fullscreen"  # Replace with the appropriate VLC command
        process = subprocess.Popen(vlc_command, shell=True)
        process.wait()
    except Exception as e:
        print(f"Error running VLC: {e}")


def run_command(command, folder_path):
    try:
        run_vlc(folder_path, command)
#        os.system(f"python3 {command}")
    except Exception as e:
        print(f"Error running command: {e}")


def draw_menu(selected_item, menu_items, menu_images):
    screen.fill((0, 0, 0))

    max_image_height = 280
    max_image_width = max_image_height

    MENU_ITEM_HEIGHT = SCREEN_HEIGHT // len(menu_items) + 100  # Adjusted MENU_ITEM_HEIGHT calculation

    for index, (text, _, image_filename) in enumerate(menu_items):
        font_color = MENU_SELECTED_COLOR if index == selected_item else MENU_TEXT_COLOR
        font = pygame.font.Font(None, MENU_FONT_SIZE)
        text_surface = font.render(text, True, font_color)
        text_rect = text_surface.get_rect()

        # Calculate the x and y coordinates based on index
        x = (SCREEN_WIDTH / len(menu_items)) * (index + 0.5)  # Adjusted x position
        y = SCREEN_HEIGHT / 2  # Adjusted y position

        # Adjust the text_rect position based on x and y
        text_rect.center = (x, y)
        screen.blit(text_surface, text_rect)

        image = menu_images.get(image_filename)
        if image:
            # Calculate the new image size while maintaining aspect ratio
            image_width, image_height = image.get_size()
            if image_width > max_image_width or image_height > max_image_height:
                ratio = min(max_image_width / image_width, max_image_height / image_height)
                new_width = int(image_width * ratio)
                new_height = int(image_height * ratio)
                image = pygame.transform.scale(image, (new_width, new_height))

            # Calculate image position below text
            image_rect = image.get_rect()
            image_rect.center = (x, y + text_rect.height // 2 - max_image_height + 100)  # Adjust the position as needed
            screen.blit(image, image_rect)

    pygame.display.flip()

'''
def draw_menu(selected_item, menu_items, menu_images):
    screen.fill((0, 0, 0))

    max_image_height = 280
    max_image_width = max_image_height

    chunk_size=3
    chunks = [menu_items[i:i + chunk_size] for i in range(0, len(menu_items), chunk_size)]

    num_rows = len(chunks)

    MENU_ITEM_HEIGHT = SCREEN_HEIGHT // num_rows + 100

    for row, chunk in enumerate(chunks):
        for index, (text, _, image_filename) in enumerate(chunk):
            overall_index = row * chunk_size + index  # Calculate the overall index
            font_color = MENU_SELECTED_COLOR if overall_index == selected_item else MENU_TEXT_COLOR
            font = pygame.font.Font(None, MENU_FONT_SIZE)
            text_surface = font.render(text, True, font_color)
            text_rect = text_surface.get_rect()
            
           # Calculate the x and y coordinates based on row and index within the current chunk
            x = (SCREEN_WIDTH // len(chunk)) * (index + 0.5)  # Adjusted x position
            y = (row + 0.5) * MENU_ITEM_HEIGHT  # Adjusted y position

            # Adjust the text_rect position based on x and y
            text_rect.center = (x, y)
            screen.blit(text_surface, text_rect)

            image = menu_images.get(image_filename)
            if image:
                # Calculate the new image size while maintaining aspect ratio
                image_width, image_height = image.get_size()
                if image_width > max_image_width or image_height > max_image_height:
                    ratio = min(max_image_width / image_width, max_image_height / image_height)
                    new_width = int(image_width * ratio)
                    new_height = int(image_height * ratio)
                    image = pygame.transform.scale(image, (new_width, new_height))

                # Calculate image position below text
                image_rect = image.get_rect()
                image_rect.center = (x, y + text_rect.height // 2 - max_image_height + 100)  # Adjust the position as needed
                screen.blit(image, image_rect)

    

    pygame.display.flip()
'''
'''
def draw_menu(selected_item, menu_items, menu_images):
    screen.fill((0, 0, 0))

    for index, (text, _, image_filename) in enumerate(menu_items):
        font_color = MENU_SELECTED_COLOR if index == selected_item else MENU_TEXT_COLOR
        font = pygame.font.Font(None, MENU_FONT_SIZE)
        text_surface = font.render(text, True, font_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, (index + 1) * MENU_ITEM_HEIGHT)

        image_rect = pygame.Rect(
            (SCREEN_WIDTH // 2) + text_rect.width // 2 + 10,  # Adjust the position as needed
            (index + 1) * MENU_ITEM_HEIGHT - IMAGE_SIZE[1] // 2,
            IMAGE_SIZE[0],  # Set the image width
            IMAGE_SIZE[1]   # Set the image height
        )

        screen.blit(text_surface, text_rect)

        image = menu_images.get(image_filename)
        if image:
            screen.blit(pygame.transform.scale(image, IMAGE_SIZE), image_rect)

    pygame.display.flip()
'''

def update_position(key):

    global selected_item, videoPlaying

    if key == "left":
           selected_item = max(0, selected_item - 1)
    elif key == "right":
            selected_item = min(len(menu_items) - 1, selected_item + 1)
    elif key == "enter": 
            selected_command = menu_items[selected_item][1]
            run_command(selected_command, folder_path)

def main():

    global menu_items, menu_images, videoPlaying  # Declare menu_items and menu_images as global

    menu_items = get_menu_items(folder_path)
    menu_images = get_menu_images(folder_path, menu_items)

    video_playing_event = multiprocessing.Event()
    
    def keyboard_listener():
        while True:
            if not video_playing_event.is_set():
                event = keyboard.read_event(suppress=True)
                if event.event_type == keyboard.KEY_DOWN:
                    if event.name == "a" or event.name == "left":
                        update_position("left")
                    elif event.name == "d" or event.name == "right":
                        update_position("right")
                    elif event.name == "enter" or event.name == "return":
                        update_position("enter")

    keyboard_thread = threading.Thread(target=keyboard_listener)
    keyboard_thread.daemon = True
    keyboard_thread.start()

    '''
    video_thread.start()
    video_thread.join()
    video_thread.close()
    '''

    while True:
        
        draw_menu(selected_item, menu_items, menu_images)

    


if __name__ == "__main__":
    main()
