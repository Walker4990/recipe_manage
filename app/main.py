from fastapi import FastAPI

from app.routers import recipes

app = FastAPI(title="Recipe API")
app.include_router(recipes.router)
