from pydantic import BaseModel


class ErrorResponse(BaseModel):
    statusCode: int
    message: str
    errors: list[str] | None = None

class ConsultaAgent(BaseModel):
    prompt: str
    
class ResponseAgent(BaseModel):
    resposta_agent: str | None = None