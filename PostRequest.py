import requests
import json
import io
import base64
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Replace 'your_url_here' with the actual URL you want to send the POST request to.
url = 'http://it099859:7860/sdapi/v1/txt2img'

# Replace 'payload_data' with the data you want to send in the POST request (if any).
payload_data = {
  "prompt": "A digital poster of a really cool movie, high resolution, 8k",
  "width": 1024,
  "height": 1024,
  "sampler_name": "DPM++ 2M Karras",
  "steps": 30,
  "batch_size": 6
}

json_data = json.dumps(payload_data)

try:
    # Send the POST request with the specified URL and data.
    response = requests.post(url, data=json_data)

    # Check the response status code to see if the request was successful (usually 200 OK).
    if response.status_code == 200:
        print("POST request was successful!")
        print("Response content:")
        #Parse the repsonse json
        response_data = response.json()
        #check if images were returned in the request, then do some stuff if they are
        if 'images' in response_data:
            #Print for debugging, can be reomved
            print(f"Image: {response_data['images']}")
            #image = Image.open(io.BytesIO(base64.b64decode(response_data['images'][0])))
            #Iterate over the number of images sent back in the response
            for i, image_string in enumerate(response_data['images']):
                #for each image, decode the base64 string, and load into memory
                image = Image.open(io.BytesIO(base64.b64decode(image_string)))
                #use whatever the built in system image viewier is to display the image
                image.show()
                image.save("image_{i}.png")
                #trying out a differnt image drawing library
                '''
                img = mpimg.imread(io.BytesIO(base64.b64decode(image_string)))
                plt.imshow(img)
                plt.show()
                plt.axis('off')  # Optional: Hide axis labels and ticks
                '''
        if 'info' in response_data:
            print(f"Info: {response_data['info']}")
    #Handle some errors, print the errors (This should probably be in a Try/Catch so that it doesnt freak out if the response isnt json)
    else:
        print(f"POST request failed with status code {response.status_code}")
        error_data = response.json()
        if 'error' in error_data and 'detail' in error_data:
            print(f"Error: {error_data['error']}")
            print(f"Detail: {error_data['detail']}")
except Exception as e:
    print(f"An error occurred: {str(e)}")
