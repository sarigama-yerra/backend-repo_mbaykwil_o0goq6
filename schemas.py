"""
Database Schemas

Pydantic models that define your MongoDB collections.
Each model name maps to a collection with the lowercase name.
Example: class User -> collection "user"
"""

from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import Optional, List

# Core marketing site content

class Service(BaseModel):
    title: str = Field(..., description="Service name")
    slug: str = Field(..., description="URL-friendly identifier")
    short: str = Field(..., description="Short blurb")
    description: Optional[str] = Field(None, description="Detailed description")
    icon: Optional[str] = Field(None, description="Lucide icon name")
    featured: bool = Field(False, description="Show in homepage highlights")

class Project(BaseModel):
    title: str = Field(...)
    slug: str = Field(...)
    summary: str = Field(...)
    image: Optional[HttpUrl] = None
    tags: List[str] = Field(default_factory=list)
    link: Optional[HttpUrl] = None
    featured: bool = Field(False)

class Testimonial(BaseModel):
    author: str = Field(...)
    role: Optional[str] = None
    quote: str = Field(...)
    company: Optional[str] = None
    avatar: Optional[HttpUrl] = None
    featured: bool = Field(True)

class Inquiry(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    phone: Optional[str] = None
    company: Optional[str] = None
    message: str = Field(..., min_length=5)
    source: Optional[str] = Field(None, description="Where the user came from")

# Example generic collections kept for reference (not used by the site directly)
class User(BaseModel):
    name: str
    email: EmailStr
    is_active: bool = True

class Product(BaseModel):
    title: str
    price: float
    in_stock: bool = True
