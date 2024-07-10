from fastapi import APIRouter, Form
from app.utils import check_thread_id, new_convo, existing_user
from twilio.twiml.messaging_response import MessagingResponse


router = APIRouter(
    prefix = "/messages",
    tags=["messages"]
)

@router.post("/messages")
async def messages(Body: str = Form(...), From: str = Form(...)):
    message = Body.strip()
    phone_number = From.strip()
    print(f"Received message from: {phone_number}: {message}")


    while True:

        if check_thread_id(phone_number):
            existing_user(phone_number, message)
            break

        if not check_thread_id:
            response = new_convo(phone_number, message)

    resp = MessagingResponse()
    resp.message(response)

    return str(resp)