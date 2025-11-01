from sqlalchemy import Column,Integer,String,Date

from db.postgres import Base    
from sqlalchemy.dialects.postgresql import JSON


class CatData(Base):

    __tablename__="cat_data"

    id=Column(Integer,primary_key=True,index=True)
    data=Column(JSON)
    photo=Column(String)
    lab_analysis=Column(JSON)
    lab_reports=Column(JSON)
    user_id=Column(Integer)