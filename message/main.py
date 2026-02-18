import uvicorn
from fastapi import FastAPI, Response

app = FastAPI()
STATIC_CONTENT = "not implemented poky sho"

@app.get("/health")
def health():
    return "ok"

@app.get("/message")
def get_msg():
    return Response(content=STATIC_CONTENT, media_type="text/plain")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8003)