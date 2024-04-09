import requests
import base64
import base64
import io
from PIL import Image

if __name__ == "__main__":
    while True:
        option = input("Enter option 1~3 or q to quit: ")
        if option == "q":
            break

        # 1. Health check
        elif option == "1":
            url = "http://localhost:8000/"
            response = requests.get(url)
            print(response.json())

        # 2. Bytes image
        elif option == "2":
            url = "http://localhost:8000/image"
            response = requests.get(url)
            # print("Binary:", response.content) # binary data
            with open("bytes_image.png", "wb") as f:
                f.write(response.content)

        # 3. Base64 image
        elif option == "3":
            url = "http://localhost:8000/image/base64"
            response = requests.get(url)
            image_data = response.json()['image']
            image_bytes = base64.b64decode(image_data)
            pil_image = Image.open(io.BytesIO(image_bytes))
            pil_image.save("base64_image.png")
        
        else:
            continue

