from sqlalchemy import Column,Integer

from db.postgres import Base    
from sqlalchemy.dialects.postgresql import JSON


class Users(Base):

    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)
    vet_notes=Column(JSON)