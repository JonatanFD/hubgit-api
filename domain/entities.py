from redis_om import Field, JsonModel
from typing import Optional
from enum import Enum

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
