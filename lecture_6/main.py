from fastapi import FastAPI
import uvicorn

app = FastAPI()
@app.get("/healthcheck")
async def healthcheck() -> dict:
    return {"status": "ok"}
