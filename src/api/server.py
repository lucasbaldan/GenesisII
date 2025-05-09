from fastapi import FastAPI
from api.controllers.iaAgentController import iaAgentControllerRouter

app = FastAPI()
app.include_router(iaAgentControllerRouter)