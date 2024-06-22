from pydantic import BaseModel

class InputSchema(BaseModel):
    param1: str
    param2: str
