from typing import Optional

from pydantic import BaseModel


class LoadExistingResponse(BaseModel):
    to_discard: list[str] = []
    best: Optional[str] = None
