from pydantic import BaseModel
from typing import Any


class GlobalResult(BaseModel):
    message: Any
