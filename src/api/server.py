from fastapi import FastAPI
from api.controllers import usuarioController, iaAgentController

app = FastAPI()
app.include_router(iaAgentController.router)
app.include_router(usuarioController.router)