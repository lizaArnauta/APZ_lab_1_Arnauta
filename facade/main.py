import uvicorn
import httpx
import uuid
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class Msg(BaseModel):
    msg: str

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/facade_post")
async def msg_post(data: Msg):
    id = str(uuid.uuid4())
    print(f"message content: {data.msg}")
    payload = {
        "uuid": id,
        "msg": data.msg
    }
    max_retries = 3
    delay = 2
    async with httpx.AsyncClient() as client:
        for attempt in range(max_retries):
            try:
                print(f"sending to logging service (attempt number {attempt + 1})")
                resp = await client.post("http://127.0.0.1:8002/log", json=payload)
                print("successful")
                return {"id": id, "status": "committed"}
            
            except httpx.RequestError:
                print(f"connection failed, retrying")
                if attempt < max_retries - 1:
                    time.sleep(delay)
                else:
                    raise HTTPException(status_code=400, detail="logging service unavailable after all retries")

@app.get("/facade_get")
async def msg_get():
    async with httpx.AsyncClient() as client:
        try:
            r1 = await client.get("http://127.0.0.1:8002/log")
            r2 = await client.get("http://127.0.0.1:8003/message")
            return f"{r1.text}  {r2.text}"
        except:
            return "services unavailable"

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)