from pydantic import BaseModel


class user_details(BaseModel):
    name:str
    email:str
    password:str
    lan:float
    lat:float