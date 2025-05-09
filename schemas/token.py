# schemas/token.py

from pydantic import BaseModel
from typing import Optional

class TokenData(BaseModel):
    id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[str] = None
