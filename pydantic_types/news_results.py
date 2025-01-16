from pydantic import BaseModel
from datetime import datetime

class Source(BaseModel):
  name: str
  url: str

class NewsResult(BaseModel):
  category: str
  headline: str
  description: str
  date: datetime
  sources: list[Source]

class NewsResults(BaseModel):
  results: list[NewsResult]