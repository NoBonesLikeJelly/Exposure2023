from PIL import Image
import os

# Set the width and height of each image
image_width = 1024
image_height = 576

# Set the number of images per row and column in the grid
images_per_row = 16
images_per_column = 4

# Set the path to the folder containing the images
folder_path = 'Sarah_Grid_Images'

# Get a list of all the image filenames in the folder
filenames = os.listdir(folder_path)

# Sort the filenames by the image number at the end of the filename
filenames = sorted(filenames, key=lambda x: int(x.split('_')[-1].split('.')[0]))


# Sort the filenames by the image number at the start of the filename
#filenames = sorted(filenames, key=lambda x: int(x.split('_')[0]))

# Calculate the size of the final grid
grid_width = image_width * images_per_row
grid_height = image_height * images_per_column
grid_size = (grid_width, grid_height)

# Create a new image to hold the grid
grid_image = Image.new('RGBA', grid_size)

# Loop through each image and paste it onto the grid
for i, filename in enumerate(filenames):
    # Open the image and resize it
    image_path = os.path.join(folder_path, filename)
    image = Image.open(image_path).convert('RGBA')
    image = image.resize((image_width, image_height))

    # Calculate the position of the image in the grid
    row = i // images_per_row
    col = i % images_per_row
    position = (col * image_width, row * image_height)

    # Paste the image onto the grid
    grid_image.paste(image, position)

# Save the final grid image
grid_image.save('grid.png')