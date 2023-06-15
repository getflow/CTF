from pydantic import BaseModel
from pydantic.typing import Optional


class SomeCommit(BaseModel):
    parent_id: Optional[str]
    message: str
    diff: str

    @property
    def partial_hash(self):
        return hash(frozenset(dict(
            parent_id=self.parent_id,
            message=self.message,
            diff=self.diff
        ).items()))
