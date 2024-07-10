from sqlalchemy import Integer, Column, String
from .database import Base
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Lead(Base):
    __tablename__ = "leads"

    thread_id = Column(String, primary_key= True, nullable=False)
    phone_number = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))