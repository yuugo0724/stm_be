from pydantic import BaseModel

class ErrorResponse(BaseModel):
  status: int
  error_code: str
  error_message: str

class HttpErrorResponse(BaseModel):
  status: int
  error_code: str
  error_message: str
  headers: dict
