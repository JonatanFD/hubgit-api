from pydantic import BaseModel


class UpdateUserNameRequest(BaseModel):
    name: str
