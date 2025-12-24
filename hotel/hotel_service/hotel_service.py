from fastapi import HTTPException,status
from hotel_schema.hotel_scheme import auth
from hotel_model.hotel_model import hotel_details
from hotel_utils.hotel_utils import hash_password,unhash
class hotel_service:
    def __init__(self,db):
        self.collection=db

    def create_details(self,singup:hotel_details):
        existing=self.collection.query(auth).filter(auth.email==singup.email).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail='Email already exists')
        password=hash_password(singup.password)
        print(existing)
        if  singup.email=='' or singup.email=='string' or singup.email.isupper() or not singup.email.endswith('@gmail.com'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='invalid input')
        if  singup.password==''or singup.password=='string':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='invalid input')
        if  singup.hotel_name==''or singup.hotel_name=='string':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='invalid input')
        if singup.hotel_des=='' or singup.hotel_des=='string':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='invalid input')
      
        new_hotel=auth(
             email=singup.email,
           password=password,
           hotel_name=singup.hotel_name,
    hotel_des=singup.hotel_des,
    lat=singup.lat,
    lan=singup.lan

        )
        self.collection.add(new_hotel)
        self.collection.commit()
        self.collection.refresh(new_hotel)

        return new_hotel
    
    def login_hotel(self,email:str,password:str):
        hotel=self.collection.query(auth).filter(auth.email==email).first()
        if not hotel:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid input')
        unhash_pass=unhash(password,hotel.password)
        if not unhash_pass:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid password')
        # hotel.is_driver_active = True
        # driver.lat = lat
        # driver.lan = lan
        self.collection.commit()
        self.collection.refresh(hotel)
        return hotel