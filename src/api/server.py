from http import HTTPStatus
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api.controllers import usuarioController, iaAgentController

app = FastAPI()
app.include_router(iaAgentController.router)
app.include_router(usuarioController.router)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content={"detail": f"Erro inesperado: {str(exc)}"},
    )