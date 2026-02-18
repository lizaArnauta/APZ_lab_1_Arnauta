import uvicorn
from fastapi import FastAPI, Response
from pydantic import BaseModel

app = FastAPI()
storage = {}

class LogRequest(BaseModel):
    uuid: str
    msg: str

@app.get("/health")
def health():
    return "ok"

@app.post("/log")
def log_post(data: LogRequest):
    if data.uuid in storage:
        print(f"message {data.uuid} already exists, so we will ignore it")
        return {"status": "already_exists"}
    storage[data.uuid] = data.msg
    print(f"log was saved: {data.msg} with id {data.uuid}")
    return {"status": "saved"}

@app.get("/log")
def log_get():
    msgs = list(storage.values())
    result = ", ".join(msgs)
    print(f"num of messages: {len(msgs)}")
    return Response(content=result, media_type="text/plain")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)