from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
import requests
import datetime

app = Flask(__name__)
CORS(app)


@app.route("/gen", methods=["GET", "POST"])
def genrate():

    data = request.json
    name = data["name"]

    from PIL import ImageFont, ImageDraw, Image
    import cv2
    import numpy as np

    f1 = open("coords.txt", "r")
    coordinates = f1.read().split("\n")

    flag = True

    name_to_print = name
    date_to_print = "19/04/2024"  # Change this date as per requirement

    # Load image in OpenCV
    image = cv2.imread("ce3.jpg")

    # Convert the image to RGB (OpenCV uses BGR)
    cv2_im_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Pass the image to PIL
    pil_im = Image.fromarray(cv2_im_rgb)

    draw = ImageDraw.Draw(pil_im)
    # use a truetype font
    font = ImageFont.truetype(
        "./fonts/MLSJN.TTF", 29
    )  # You can change fonts from list given bottom
    font1 = ImageFont.truetype("./fonts/OLDENGL.TTF", 22)

    # Draw the text
    draw.text(
        (int(coordinates[0]), int(coordinates[1])), name_to_print, font=font, fill="red"
    )
    draw.text(
        (int(coordinates[2]), int(coordinates[3])),
        date_to_print,
        font=font1,
        fill="blue",
    )

    # Get back the image to OpenCV
    cv2_im_processed = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)

    if flag:
        cv2.imshow("Certificate", cv2_im_processed)  # Shows sample image
        flag = False
    path = ""
    cv2.imwrite("./output/" + "file" + ".png", cv2_im_processed)

    def savenft(path):

        with open(path, "rb") as f:
            image_data = f.read()

        # Create FormData-like object
        files = {"file": ("filename.jpg", image_data)}  # Adding the filename here

        # Define headers (without Content-Type)
        headers = {
            "Authorization": "Your_key",
        }

        # Make the request
        response = requests.post(
            "https://api.nft.storage/upload", files=files, headers=headers
        )

        cid = response.json()["value"]["cid"]

        value = f"https://{cid}.ipfs.nftstorage.link/filename.jpg"

        return value

    value = savenft(
        "C:/Users/shrey/OneDrive/Desktop/Certificate-Automation-Using-Python-master/output/file.png"
    )

    return value


if __name__ == "__main__":
    app.run(host="0.0.0.0")
