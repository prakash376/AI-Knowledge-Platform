from sqlalchemy import Column, String, Boolean, DateTime
from datetime import datetime

from database.database import Base

class User(Base):

    __tablename__ = "users"

    id = Column(String, primary_key = True)
    email =Column(String, unique = True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    

class Document(Base):

    __tablename__ = "documents"

    id = Column(String, primary_key = True)
    owner_id = Column(String, nullable = False)
    filename = Column(String, nullable = False)
    file_path = Column(String, nullable = False)
    status = Column(String, default = "uploading")    
    created_at = Column(DateTime, default = datetime.utcnow)