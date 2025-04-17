from pydantic import BaseModel


class Contact(BaseModel):
    id: int
    first: str | None
    last: str | None
    phone: str | None
    email: str
    errors: dict
