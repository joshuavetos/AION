from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    path: str = Field(..., description="Absolute path to the text file to analyze")
