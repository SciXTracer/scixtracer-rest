from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import datasets
from .routers import queries
from .routers import data

app = FastAPI(dependencies=[])

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(datasets.router)
app.include_router(queries.router)
app.include_router(data.router)


@app.get("/")
async def root():
    return {"message": "SciXTracer RESTful API"}
