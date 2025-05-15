from fastapi import FastAPI
from api.controllers.iaAgentController import iaAgentControllerRouter
from api.controllers.usuarioController import usuarioController

app = FastAPI()
app.include_router(iaAgentControllerRouter)
app.include_router(usuarioController)

@app.post("/teste")
async def teste():
    return {"message": "Hello World!"}