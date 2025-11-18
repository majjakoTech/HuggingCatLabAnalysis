from sqlalchemy import Column,Integer,String,Date,Text

from db.postgres import Base    
from sqlalchemy.dialects.postgresql import JSON


class CatData(Base):

    __tablename__="cat_data"

    id=Column(Integer,primary_key=True,index=True)
    data=Column(JSON)
    photo=Column(String)
    lab_reports=Column(JSON)
    key_findings=Column(Text)
    overview_lab_analysis=Column(Text)
    user_id=Column(Integer)
    created_at=Column(Date)
    updated_at=Column(Date)