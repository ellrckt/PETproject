from pydantic import BaseModel


class TokenInfo(BaseModel):

    access_token: str | None = None
    refresh_token: str | None = None
    id: int | None = None
    token_type: str = "Bearer"
