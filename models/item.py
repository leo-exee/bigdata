from pydantic import BaseModel


class ItemOutDTO(BaseModel):
    word: str
    count: int
