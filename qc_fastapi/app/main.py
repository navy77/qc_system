from fastapi import FastAPI
from .database import engine
from . import models
from .routers import specification
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(specification.router, prefix="/specification", tags=["specification"])
# app.include_router(measure.router, prefix="/measure", tags=["measure"])
# app.include_router(calibration.router, prefix="/calibration", tags=["calibration"])

origins = [
    "http://localhost:3000",  
    "http://localhost:8000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)