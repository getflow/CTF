from pydantic import BaseModel


class SomeCommit(BaseModel):
    parent_id: str
    message: str
    diff: str

    @property
    def partial_hash(self):
        return hash(self)
