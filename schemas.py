"""
Database Schemas for the Ebook Platform

Each Pydantic model represents a collection in MongoDB.
Collection name is the lowercase of the class name (e.g., User -> "user").
"""

from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import Optional, List, Literal, Dict
from datetime import datetime


# ---------- Core Domain Schemas ----------

class User(BaseModel):
    """
    Users collection schema
    - role supports RBAC: "user" or "admin"
    """
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    hashed_password: str = Field(..., min_length=60, max_length=200, description="BCrypt hashed password")
    role: Literal["user", "admin"] = Field("user", description="Role-based access control")
    avatar_url: Optional[HttpUrl] = None
    is_active: bool = True


class Ebook(BaseModel):
    """
    Ebooks available for purchase/reading
    """
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=120)
    description: Optional[str] = Field(None, max_length=5000)
    price: float = Field(..., ge=0)
    currency: Literal["INR", "USD"] = "INR"
    cover_url: Optional[HttpUrl] = None
    file_urls: Dict[str, HttpUrl] = Field(default_factory=dict, description="Keys: pdf, epub")
    categories: List[str] = Field(default_factory=list)
    published: bool = True
    created_by: Optional[str] = Field(None, description="Creator user id")


class Purchase(BaseModel):
    """
    Records of user purchases
    """
    user_id: str
    ebook_id: str
    amount: float = Field(..., ge=0)
    currency: Literal["INR", "USD"] = "INR"
    status: Literal["created", "paid", "failed", "refunded"] = "created"
    razorpay_order_id: Optional[str] = None
    razorpay_payment_id: Optional[str] = None
    razorpay_signature: Optional[str] = None


class LibraryItem(BaseModel):
    """
    A user's library entry linking to ebooks they own
    """
    user_id: str
    ebook_id: str
    last_read_at: Optional[datetime] = None
    progress: float = Field(0, ge=0, le=100)


# ---------- Helper: API Schema Introspection ----------

class SchemaInfo(BaseModel):
    name: str
    schema: dict
