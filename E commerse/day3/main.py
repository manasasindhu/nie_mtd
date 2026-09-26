from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from pymongo import MongoClient
from bson import ObjectId


# =========================
# APP
# =========================

app = FastAPI(title="E-Commerce Ticket System")


# =========================
# MONGODB CONFIGURATION
# =========================

URL = "mongodb://127.0.0.1:27017"

client = MongoClient(URL)

db = client["ecommerce_db"]

ticket_collection = db["tickets"]


# =========================
# PYDANTIC SCHEMAS
# =========================

class TicketCreate(BaseModel):
    customer_name: str
    product_name: str
    rating: int
    comment: str
    category: str
    status: str


class TicketResponse(TicketCreate):
    id: str


# =========================
# HELPER FUNCTION
# =========================

def ticket_helper(ticket_doc):
    return {
        "id": str(ticket_doc["_id"]),
        "customer_name": ticket_doc["customer_name"],
        "product_name": ticket_doc["product_name"],
        "rating": ticket_doc["rating"],
        "comment": ticket_doc["comment"],
        "category": ticket_doc["category"],
        "status": ticket_doc["status"]
    }


# =========================
# CREATE TICKET
# =========================

@app.post(
    "/tickets",
    status_code=201,
    response_model=TicketResponse
)
def ticket_create(payload: TicketCreate):

    ticket_dict = payload.model_dump()

    result = ticket_collection.insert_one(ticket_dict)

    new_ticket = ticket_collection.find_one(
        {"_id": result.inserted_id}
    )

    return ticket_helper(new_ticket)


# =========================
# GET ALL TICKETS
# =========================

@app.get(
    "/tickets",
    response_model=list[TicketResponse]
)
def ticket_read_all():

    documents = ticket_collection.find()

    tickets = [
        ticket_helper(document)
        for document in documents
    ]

    return tickets


# =========================
# GET TICKET BY ID
# =========================

@app.get(
    "/tickets/{id}",
    response_model=TicketResponse
)
def ticket_read_by_id(id: str):

    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=400,
            detail="Invalid Ticket ID"
        )

    ticket = ticket_collection.find_one(
        {"_id": ObjectId(id)}
    )

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket Not Found"
        )

    return ticket_helper(ticket)


# =========================
# UPDATE TICKET
# =========================

@app.put(
    "/tickets/{id}",
    response_model=TicketResponse
)
def ticket_update(
    id: str,
    payload: TicketCreate
):

    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=400,
            detail="Invalid Ticket ID"
        )

    ticket_dict = payload.model_dump()

    result = ticket_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": ticket_dict}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Ticket Not Found"
        )

    updated_ticket = ticket_collection.find_one(
        {"_id": ObjectId(id)}
    )

    return ticket_helper(updated_ticket)


# =========================
# DELETE TICKET
# =========================

@app.delete("/tickets/{id}")
def ticket_delete(id: str):

    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=400,
            detail="Invalid Ticket ID"
        )

    result = ticket_collection.delete_one(
        {"_id": ObjectId(id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Ticket Not Found"
        )

    return {
        "message": "Ticket Deleted Successfully"
    }