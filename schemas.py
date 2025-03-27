from typing import Optional
from pydantic import BaseModel

class CustomerCreate(BaseModel):
    name: str
    phone: Optional[str]
    email: Optional[str]
    company: Optional[str]
    address: Optional[str]
    tags: Optional[str]

class MessageCreate(BaseModel):
    message: str
    sender: Optional[str]

class TicketCreate(BaseModel):
    customer_id: int
    subject: str
    description: str
