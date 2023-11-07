import pygame
import os
import sys
import subprocess

# Initialize pygame
pygame.init()

# Constants
monitor_info = pygame.display.Info()
SCREEN_WIDTH = monitor_info.current_w
SCREEN_HEIGHT = monitor_info.current_h

IMAGE_SIZE = (150, 150)  # Set the desired image size
MENU_ITEM_HEIGHT = 160  # Set the height of each menu item (including padding)

MENU_FONT_SIZE = 36
MENU_ITEM_SPACING = 50
MENU_TEXT_COLOR = (255, 255, 255)
MENU_SELECTED_COLOR = (0, 255, 0)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
#screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu")


def run_vlc(folder_path, video_file):
    try:
        vlc_command = f"/Applications/VLC.app/Contents/MacOS/VLC {folder_path}{video_file} --no-repeat --play-and-exit --fullscreen"  # Replace with the appropriate VLC command
        subprocess.Popen(vlc_command, shell=True)
    except Exception as e:
        print(f"Error running VLC: {e}")

# Define the menu items and corresponding commands
def get_menu_items(folder_path):
    menu_items = []
    for filename in os.listdir(folder_path):
        if not filename.endswith(".png") and not filename.endswith(".DS_Store") and os.path.isfile(os.path.join(folder_path, filename)):
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

def run_command(command, folder_path):
    try:
        run_vlc(folder_path, command)
#        os.system(f"python3 {command}")
    except Exception as e:
        print(f"Error running command: {e}")

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
#        print(f"Loading Image for {text}: {image}")
        if image:
            screen.blit(pygame.transform.scale(image, IMAGE_SIZE), image_rect)
            '''
            image_rect = image.get_rect()
            image_rect.x = (SCREEN_WIDTH // 2) + text_rect.width // 2 + 10  # Adjust the position as needed
            image_rect.centery = text_rect.centery
            screen.blit(image, image_rect)
            '''

    pygame.display.flip()

def main():
    selected_item = 0

    folder_path = "./TestExposureRaspi/"
    menu_items = get_menu_items(folder_path)
    menu_images = get_menu_images(folder_path, menu_items)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_item = max(0, selected_item - 1)
                elif event.key == pygame.K_DOWN:
                    selected_item = min(len(menu_items) - 1, selected_item + 1)
                elif event.key == pygame.K_RETURN:
                    selected_command = menu_items[selected_item][1]
                    run_command(selected_command, folder_path)

        draw_menu(selected_item, menu_items, menu_images)

if __name__ == "__main__":
    main()
