import tifffile as tiff
from PIL import Image

def split_tiff(input_path, output_prefix, square_size):
    # Open the input TIFF image
    input_image = tiff.imread(input_path)

    # Get the dimensions of the input image
    height, width = input_image.shape[:2]

    # Calculate the number of squares horizontally and vertically
    num_squares_x = width // square_size
    num_squares_y = height // square_size

    # Iterate over each square
    for y in range(num_squares_y):
        for x in range(num_squares_x):
            # Calculate the coordinates of the current square
            left = x * square_size
            upper = y * square_size
            right = left + square_size
            lower = upper + square_size

            # Crop the square from the input image
            square = input_image[upper:lower, left:right]

            # Convert the square to a PIL Image
            square_image = Image.fromarray(square)

            # Save the square as a new PNG file
            output_path = f"{output_prefix}_{x}_{y}.png"
            square_image.save(output_path, format='PNG')
            print(f"Saved {output_path}")

# Usage example
input_path = "Square_0.75M_Aerial_Export.tif"
output_prefix = "output_square"
square_size = 8192

split_tiff(input_path, output_prefix, square_size)
