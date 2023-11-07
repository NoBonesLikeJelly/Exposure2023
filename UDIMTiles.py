import tifffile as tiff
from tqdm import tqdm
from PIL import Image

def split_image_into_tiles(image_path, output_dir):

    image = tiff.imread(image_path)
    image = image.astype('uint8')

    width, height = image.shape[1], image.shape[0]
    tile_width = width // 4
    tile_height = height // 4

    tile_number = 1001
    for row in tqdm(range(4), desc="Rows"):
        tile_number_start = tile_number  # Store the starting tile number for the row
        for col in tqdm(range(4), desc="Columns", leave=False):
            x = col * tile_width
            y = height - (row + 1) * tile_height
            tile = image[y:y+tile_height, x:x+tile_width, :]

            tile_number_mod = tile_number + row * 10
            
            # Create PIL Image from numpy array
            tile = Image.fromarray(tile)

            if tile_number_mod in special_tiles:
                tile = tile.resize(special_resolution, Image.ANTIALIAS)
            else:
                tile = tile.resize(tile_resolution, Image.ANTIALIAS)
            
            tile.save(f"{output_dir}/tile_{tile_number_mod}.png")
            print(f"Saved {output_dir}/tile_{tile_number_mod}.png")
            tile_number += 1
        tile_number = tile_number_start


# Example usage
image_path = "/Users/twilliams/Downloads/lds-wellington-region-6layers-GTiff-JPEG-SHP/EXPORTS/Square_0.75M_Aerial_Export.tif"
output_dir = "/Users/twilliams/Downloads/lds-wellington-region-6layers-GTiff-JPEG-SHP/EXPORTS/TestUdims/"
tile_resolution = (2048, 2048)
special_resolution = (8192, 8192)
special_tiles = [1012, 1013, 1022, 1023]
split_image_into_tiles(image_path, output_dir)



