from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlmodel import select
from database import init_db, get_session
from models import Customer, Message, Ticket
from schemas import CustomerCreate, MessageCreate, TicketCreate

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/customers", response_model=Customer)
def create_customer(data: CustomerCreate, session=Depends(get_session)):
    customer = Customer(**data.dict())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@app.get("/customers", response_model=List[Customer])
def list_customers(keyword: str = "", session=Depends(get_session)):
    statement = select(Customer)
    if keyword:
        statement = statement.where(Customer.name.contains(keyword))
    return session.exec(statement).all()

@app.get("/customers/{customer_id}", response_model=Customer)
def get_customer(customer_id: int, session=Depends(get_session)):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="客户不存在")
    return customer

@app.post("/customers/{customer_id}/messages")
def add_message(customer_id: int, data: MessageCreate, session=Depends(get_session)):
    message = Message(customer_id=customer_id, **data.dict())
    session.add(message)
    session.commit()
    return {"message": "沟通记录已保存"}

@app.post("/tickets", response_model=Ticket)
def create_ticket(data: TicketCreate, session=Depends(get_session)):
    ticket = Ticket(**data.dict())
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket

@app.post("/tickets/{ticket_id}/resolve")
def resolve_ticket(ticket_id: int, session=Depends(get_session)):
    ticket = session.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="工单不存在")
    ticket.is_resolved = True
    session.commit()
    return {"message": "工单已关闭"}
