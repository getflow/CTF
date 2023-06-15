from pydantic import BaseModel


class SomeProject(BaseModel):
    name: str
    description: str
