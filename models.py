from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Customer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    address: Optional[str] = None
    tags: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    message: str
    sender: Optional[str] = "系统"
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Ticket(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    subject: str
    description: str
    is_resolved: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
