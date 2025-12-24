from database import base
from sqlalchemy import String,Float,Column
class auth(base):

    __tablename__='hotel_details'

    hotel_name=Column(String,primary_key=True)
    hotel_des=Column(String,nullable=False)
    email=Column(String,nullable=False)
    password=Column(String,nullable=False)
    lan=Column(Float,nullable=False)
    lat=Column(Float,nullable=False)