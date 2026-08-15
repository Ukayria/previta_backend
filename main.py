from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.symptoms import router as symptoms_router
from routers.auth import router as auth_router

app = FastAPI(title="PreVita API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(symptoms_router)
app.include_router(auth_router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "PreVita API"}