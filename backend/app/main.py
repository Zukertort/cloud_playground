from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, posts, model, analytics, dashboard

app = FastAPI()

# Config CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(model.router)
app.include_router(analytics.router)
app.include_router(dashboard.router)

@app.get("/")
def read_root():
    return {"message": "Cloud Playground API v0.1"}