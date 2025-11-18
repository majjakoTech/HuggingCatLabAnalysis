from sqlalchemy import Column,Integer,String,Date,Text

from db.postgres import Base    
from sqlalchemy.dialects.postgresql import JSON


class VetNote(Base):

    __tablename__="vet_notes"

    id=Column(Integer,primary_key=True,index=True)
    analysis=Column(JSON)
    transcript=Column(Text)
    audio=Column(String)
    user_id=Column(Integer)
    created_at=Column(Date)