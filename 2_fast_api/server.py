import uvicorn
from fastapi import FastAPI
from PIL import Image
from fastapi.responses import StreamingResponse
import io
import base64
from pydantic import BaseModel

app = FastAPI()

IMAGE_PATH = "./2_fast_api/image.png"

# 1. Health check
@app.get("/")
def health_check():
    return {"status": 200,
            "message": "Server is running"}


# 2. Reponse binary(bytes) image
@app.get("/image")
def get_image_binary():
    try:
        image = Image.open(IMAGE_PATH)
        byte_buf = io.BytesIO()
        image.save(byte_buf, format="PNG")
        byte_buf.seek(0)
        return StreamingResponse(content=byte_buf, media_type="image/png")
    except Exception as e:
        print("Error:", e)
        return { "status": 500,
                "message": "Error occured",
                "error": str(e) }

# 3. Reponse string(base64) image
@app.get("/image/base64")
def get_image_base64():
    try:
        image = Image.open(IMAGE_PATH)
        byte_buf = io.BytesIO()
        image.save(byte_buf, format="PNG")
        base64_img = base64.b64encode(byte_buf.getvalue()).decode("utf-8")
        return { "status": 200,
                "message": "Image converted to base64",
                "image": base64_img }
    except Exception as e:
        print("Error:", e)
        return { "status": 500,
                "message": "Error occured",
                "error": str(e) }


# 4. Request with payload
class UserPayload(BaseModel):
    user_id: str
    age: int

@app.post("/user")
def create_user(user: UserPayload):
    # Do something..
    print("id:", user.user_id,"age:", user.age)
    return { "status": 200,
            "message": "User created",
            "data": user.user_id }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)