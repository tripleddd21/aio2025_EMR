from fastapi import FastAPI, APIRouter
import uvicorn

router = APIRouter()

@router.get("/ping")
def ping():
    return {"message": "pong"}

# ✅ Cho phép chạy trực tiếp file này
if __name__ == "__main__":
    app = FastAPI()
    app.include_router(router)

    uvicorn.run(app, host="127.0.0.1", port=8000)
