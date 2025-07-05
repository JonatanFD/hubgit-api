import uuid
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

from redis_om import Field, JsonModel
from typing import Optional, Any, Self
from enum import Enum

from resources.create_post_resource import CreatePostResource

# Cargar variables de entorno
load_dotenv()

# Configurar Redis-OM una sola vez al importar el módulo
_redis_configured = False
if not _redis_configured:
    from redis_setup.redis_config import configure_redis_om
    configure_redis_om()
    _redis_configured = True


class UserRole(str, Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"
    MODERATOR = "moderator"


class User(JsonModel):
    id: str = Field(index=True)
    name: str = Field(index=True)
    email: str = Field(index=True)
    role: UserRole = Field(index=True)
    company_id: str = Field(index=True)

    class Meta:
        model_key_prefix = "user"


class Company(JsonModel):
    id: str = Field(index=True)
    name: str = Field(index=True)
    admin_id: str = Field(index=True)
    employees: list[str] = Field(index=True)

    class Meta:
        model_key_prefix = "company"


class Post(JsonModel):
    id: str = Field(index=True)
    title: str = Field(index=True)
    description: str = Field(index=True)
    author_id: str = Field(index=True)
    company_id: str = Field(index=True)
    tags: list[str] = Field(index=True)
    views: int = Field(index=True)
    likes: int = Field(index=True)
    comments_count: int = Field(index=True)
    created_at: str = Field(index=True)

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
    id: str = Field(index=True)
    post_id: str = Field(index=True)
    author_id: str = Field(index=True)
    company_id: str = Field(index=True)
    content: str = Field(index=True)
    parent_comment_id: Optional[str] = Field(index=True)
    likes: int = Field(index=True)
    created_at: str = Field(index=True)
    updated_at: Optional[str] = Field(index=True)

    class Meta:
        model_key_prefix = "comment"
