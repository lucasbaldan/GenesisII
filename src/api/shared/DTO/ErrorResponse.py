from pydantic import BaseModel


class ErrorResponse(BaseModel):
    statusCode: int
    message: str
    errors: list[str] | None = None