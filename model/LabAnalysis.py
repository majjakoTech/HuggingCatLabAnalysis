from sqlalchemy import Column,Integer,String,Date

from db.postgres import Base    
from sqlalchemy.dialects.postgresql import JSON


class LabAnalysis(Base):

    __tablename__="lab_analysis"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    data=Column(JSON)
    cat_data_id=Column(Integer)
    created_at=Column(Date)
