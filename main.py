from fastapi import FastAPI

from routes import router as bus_router

app = FastAPI()

app.include_router(bus_router)