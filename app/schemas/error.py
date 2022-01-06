from typing import Optional

from pydantic import BaseModel


class HTTPError(BaseModel):
    detail: Optional[str]
