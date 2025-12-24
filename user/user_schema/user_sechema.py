from database import base
from sqlalchemy import String,Float,Column
class auth(base):

    __tablename__='user_details'

    name=Column(String,nullable=False)
    email=Column(String,primary_key=True)
    password=Column(String,nullable=False)
    lan=Column(Float,nullable=False)
    lat=Column(Float,nullable=False)