from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    path: str
