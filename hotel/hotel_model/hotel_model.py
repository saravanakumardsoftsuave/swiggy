from pydantic import BaseModel


class hotel_details(BaseModel):
    hotel_name:str
    hotel_des:str
    email:str
    password:str
    lan:float
    lat:float