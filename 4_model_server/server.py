from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from ultralytics import YOLO
from PIL import Image
from io import BytesIO
import torch
import uvicorn
import model
import utils

yolo_model: YOLO = model.load_model()

class ImagePayload(BaseModel):
    image: str

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": 200,
            "message": "Server is running"}


@app.post("/inference/base64")
def inference_endpoint_base64(image_payload: ImagePayload):
    global yolo_model
    img = utils.base64_to_pillow_image(image_payload.image)

    result = model.inference(yolo_model, img)

    return {"status":200,"result": result}


@app.post("/inference")
async def inference_endpoint(file: UploadFile = File()):
    global yolo_model
    contents = await file.read()
    image = Image.open(BytesIO(contents))

    result = model.inference(yolo_model, image)

    return {"status":200,"result": result}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
