from pydantic import BaseModel


class RegisterForm(BaseModel):
    maker: str
    bow_kind: str | None = None
    owner: str | None = None
