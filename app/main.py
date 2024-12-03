import importlib
import os
from fastapi import FastAPI

functions_path = os.path.join(os.path.dirname(__file__), "functions")
for filename in os.listdir(functions_path):
    if filename.endswith(".py") and filename != "__init__.py":
        print(f"Loading function: {filename}")
        module_name = f"app.functions.{filename[:-3]}"
        importlib.import_module(module_name)

from app.routers.dynamic_routes import router

app = FastAPI()
app.include_router(router)
