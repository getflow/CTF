from pydantic import BaseModel


class SomeUser(BaseModel):
    name: str
    password: str
