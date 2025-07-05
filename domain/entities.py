import uuid
from datetime import datetime, timezone

from redis_om import Field, JsonModel
from typing import Optional, Any, Self
from enum import Enum

from resources.create_post_resource import CreatePostResource

# La configuración de Redis se hace en redis_config.py y se importa antes
# de importar este módulo en main.py


class UserRole(str, Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"
    MODERATOR = "moderator"


class User(JsonModel):
    id: str = Field()
    name: str = Field()
    email: str = Field()
    role: UserRole = Field()
    company_id: str = Field()

    class Meta:
        model_key_prefix = "user"


class Company(JsonModel):
    id: str = Field()
    name: str = Field()
    admin_id: str = Field()
    employees: list[str] = Field()

    class Meta:
        model_key_prefix = "company"


class Post(JsonModel):
    id: str = Field()
    title: str = Field()
    description: str = Field()
    author_id: str = Field()
    company_id: str = Field()
    tags: list[str] = Field()
    views: int = Field()
    likes: int = Field()
    comments_count: int = Field()
    created_at: str = Field()

    class Meta:
        model_key_prefix = "post"

    @classmethod
    def createFromResource(cls, post_resource: CreatePostResource):
        return Post(
            id=str(uuid.uuid4()),
            title=post_resource.title,
            description=post_resource.description,
            author_id=post_resource.author_id,
            company_id=post_resource.company_id,
            tags=post_resource.tags,
            views=0,
            likes=0,
            comments_count=0,
            created_at=datetime.now(timezone.utc).isoformat()
        )

class Comment(JsonModel):
    id: str = Field()
    post_id: str = Field()
    author_id: str = Field()
    company_id: str = Field()
    content: str = Field()
    parent_comment_id: Optional[str] = Field()
    likes: int = Field()
    created_at: str = Field()
    updated_at: Optional[str] = Field()

    class Meta:
        model_key_prefix = "comment"
