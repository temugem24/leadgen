from sqlalchemy.orm import Session
from fastapi import Depends
from . import models
from app.database import get_db
from app.managers import manager
from app.assistant import AssistantManager

def check_thread_id(phone_number: int, db: Session = Depends(get_db)):
    user = db.query(models.Lead).filter(models.Lead.phone_number == phone_number).first()
    if user:
        thread_id = user.thread_id
    
    return thread_id


def new_user(phone_number: int, db: Session = Depends(get_db)):
    thread_id = manager.create_thread()
    new_user = models.Lead(thread_id=thread_id, phone_number=phone_number)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return thread_id

def new_convo(phone_number, message):
    new_thread_id = new_user(phone_number)
    manager.add_message_to_thread(thread_id=new_thread_id, role="user", content=message)
    manager.run_assistant(new_thread_id)
    response = manager.wait_for_completion(new_thread_id)

    return response

def existing_user(phone_number, message):
    new_manager = AssistantManager()
    thread_id = check_thread_id(phone_number)
    new_manager.add_message_to_thread(thread_id=thread_id, role="user", content=message)
    new_manager.run_assistant(thread_id)
    response = new_manager.wait_for_completion(thread_id)

    return response
