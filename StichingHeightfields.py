import os
from PIL import Image

# set the path of the folder containing the TIFF images
folder_path = "/Users/twilliams/Downloads/lds-wellington-city-2layers-GTiff-JPEG/wellington-city-lidar-1m-dem-2019-2020/TIFFS/"

# create a dictionary to store the images based on their position in the grid
image_dict = {}

# loop through the files in the folder
for filename in os.listdir(folder_path):
    # check if the file is a TIFF image
    if filename.endswith(".tif"):
        # extract the row and column numbers from the filename
        row_num = int(filename[-7])
        col_num = int(filename[-6] + filename[-5])

        print(filename, row_num, col_num)
        
        # open the image using the Pillow library
        image = Image.open(os.path.join(folder_path, filename))
        
        # store the image in the dictionary
        image_dict[(row_num, col_num)] = image

# determine the dimensions of the output image
max_row = max([pos[0] for pos in image_dict.keys()])
max_col = max([pos[1] for pos in image_dict.keys()])

# create a new image to hold the stitched image
output_image = Image.new("RGBA", (max_col*image.width, max_row*image.height))

# loop through the positions in the grid and paste the corresponding image onto the output image
for row in range(1, max_row+1):
    for col in range(1, max_col+1):
        image = image_dict.get((row, col))
        if image:
            output_image.paste(image, ((col-1)*image.width, (row-1)*image.height))

# save the output image
output_image.save("output.tif")
