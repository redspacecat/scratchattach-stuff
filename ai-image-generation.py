import json
import os
import time
import random
import requests
from PIL import Image
import scratchattach as scratch3

main_directory = os.path.split(os.path.abspath(__file__))[0] # Gets current directory.


session_id = [REDACTED]
username = [USERNAME]

session = scratch3.Session(session_id, username=username) #replace with your session_id and username
conn = session.connect_cloud("[YOUR PROJECT ID HERE]") #replace with your project id

client = scratch3.CloudRequests(conn)

@client.request
def ping(): #called when client receives request
    print("Ping request received")
    return "pong" #sends back 'pong' to the Scratch project

@client.request
def generate_image(username, prompt):
    print(f'{username} requested image for the prompt "{prompt}"')
    # try:
    payload = {
    "model": "dalle-3",
    "prompt": "placeholder",
    }

    headers = {
        'Content-Type': 'application/json',
    }


    payload["prompt"] = prompt

    print("Generating...")
    response = requests.post("https://reverse.mubi.tech/images/generations", json=payload, headers=headers).text #generate image and get url
    try:
        img_url = str(json.loads(response)["url"])
        print("Retrieving image...")  #retrieve image to local computer
        r = requests.get(img_url)
        print(f"Image url: {img_url}")
        image_name = f"image-{random.randint(0, 10000000)}.png" #give image unique id
        with open(os.path.join(main_directory, "images", image_name), "wb") as f:  #store image
            f.write(r.content)

        return [img_url, image_name] #return image data
        
    except Exception:
        print("There was a error.")
        return "There was a error."

@client.request
def get_image_piece(img_id, y_offset, amount, img_size): #call this function with different amounts of offset to get the image
    img = Image.open(os.path.join(main_directory, "images", img_id)).convert("RGBA") #open image based on id
    img = img.resize((int(img_size), int(img_size)))
    width, height = img.size
    pixels = img.load()

    colors = [] #construct colors list
    for y in range(int(y_offset), int(y_offset) + int(amount)): #get a specific chunk of the image
        for x in range(width):
            r, g, b, a = pixels[x, y]
            color = a * 16777216 + r * 65536 + g * 256 + b
            colors.append(color)
    return colors #return data

@client.event
def on_ready():
    print("Request handler is running")

client.run()
