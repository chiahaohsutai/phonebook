from uuid import uuid4

from pydantic import BaseModel, Field


def uid() -> str:
    """Generate a unique identifier."""
    return str(uuid4())


class Contact(BaseModel):
    id: str = Field(default_factory=uid, description="Contact ID", alias="_id")
    first: str | None = Field(default=None, description="First name")
    last: str | None = Field(default=None, description="Last name")
    phone: str | None = Field(default=None, description="Phone number")
    email: str = Field(default="", description="Email address")
    errors: dict = Field(default_factory=dict, description="Validation errors")
