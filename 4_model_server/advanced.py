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

yolo_model: YOLO = None

class ImagePayload(BaseModel):
    image: str

def on_startup():
    global yolo_model
    logging.basicConfig(level=logging.INFO)
    yolo_model = model.load_model()
    if torch.cuda.is_available():
        yolo_model = yolo_model.to("cuda")

def on_shutdown():
    global yolo_model
    del yolo_model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

@asynccontextmanager
async def lifespan(app: FastAPI):
    on_startup()
    yield
    on_shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def health_check():
    return {"status": 200,
            "message": "Server is running"}

@app.post("/inference/base64")
def inference_endpoint_base64(image_payload: ImagePayload):
    try:
        global yolo_model
        img = utils.base64_to_pillow_image(image_payload.image)
        result = model.inference(yolo_model, img)
        return {"status":200,"result": result}
    except Exception as e:
        logging.error(f"Inference Error: {e}")
        return {"status":500,"error": str(e)}

@app.post("/inference")
async def inference_endpoint(file: UploadFile = File()):
    try:
        global yolo_model
        contents = await file.read()
        image = Image.open(BytesIO(contents))
        result = model.inference(yolo_model, image)
        return {"status":200,"result": result}
    except Exception as e:
        logging.error(f"Inference Error: {e}")
        return {"status":500,"error": str(e)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
