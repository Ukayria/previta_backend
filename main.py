# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.symptoms import router

app = FastAPI(title="PreVita API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lock this down before production
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "PreVita API"}