from contextlib import asynccontextmanager
from fastapi import FastAPI
from asyncio import Event, Queue, create_task, gather, sleep, Future
from datetime import datetime

request_queue = Queue()
shutdown_event = Event()

CONCURRENT_LIMIT = 2
workers = []

async def worker():
    while not shutdown_event.is_set():
        request_id, future, request_data = await request_queue.get()
        current_datetime = datetime.now().strftime("%H:%M:%S.%f")
        print(f"Processing: {request_id} at {current_datetime}")
        await sleep(4)  # Simulate async I/O operation
        current_datetime = datetime.now().strftime("%H:%M:%S.%f")
        print(f"Done: {request_id} at {current_datetime}")
        result = {"processed_data": request_data, "timestamp": current_datetime}
        future.set_result(result)
        request_queue.task_done()
    print("Worker shutdown gracefully.")

def startup_event():
    global workers
    for _ in range(CONCURRENT_LIMIT):
        task = create_task(worker())
        workers.append(task)

async def on_shutdown():
    global shutdown_event
    shutdown_event.set()
    await request_queue.join()
    for worker in workers:
        worker.cancel()
    await gather(*workers, return_exceptions=True)
    print("Shutdown complete.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    startup_event()
    yield
    await on_shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def health_check():
    return {"status": 200,
            "message": "Server is running"}

@app.get("/limit")
async def limited_endpoint():
    current_datetime = datetime.now().strftime("%H:%M:%S.%f")
    request_id = current_datetime
    future = Future()
    await request_queue.put((request_id, future, None))
    result = await future  # Wait for the worker to process the request
    return {"request_id": request_id, **result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
