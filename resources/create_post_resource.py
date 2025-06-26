from pydantic import BaseModel

class CreatePostResource(BaseModel):
    title: str
    description: str
    tags: list[str]
    author_id: str
    company_id: str