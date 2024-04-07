import uvicorn
from fastapi import FastAPI
import time
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
app = FastAPI()
WAIT_DELAY = 3

# Global variable/state
cnt = 0

# 1. Health check
@app.get("/")
def health_check():
    return {"status": 200,
            "message": "Server is running"}

# 2. Sync sleep
@app.get("/sync")
def sleep_sync():
    time.sleep(WAIT_DELAY)
    return {"status": 200,
            "message": "Sync sleep done"}

# 3. Async sleep
@app.get("/async")
async def sleep_async():
    await asyncio.sleep(WAIT_DELAY)
    return {"status": 200,
            "message": "Async sleep done"}

# 4. Async with state
@app.get("/async/state")
async def sleep_async():
    global cnt
    # cnt += 1
    await asyncio.sleep(WAIT_DELAY)
    logging.info(f"cnt:{cnt}")
    # cnt += 1
    return {"status": 200,
            "message": "Async sleep done"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)