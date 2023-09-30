from fastapi import FastAPI
from Routers import adin_routers as adin



app = FastAPI()

app.include_router(adin.router, prefix="/adin.ai", tags=["Adin.ai"])