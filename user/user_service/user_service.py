from fastapi import HTTPException,status
from user_schema.user_sechema import auth
from user_model.user_model import user_details
from user_utils.user_utils import hash_password,unhash
class user_service:
    def __init__(self,db):
        self.collection=db

    def create_details(self,singup:user_details):
        existing=self.collection.query(auth).filter(auth.email==singup.email).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail='Email already exists')
        password=hash_password(singup.password)
        print(existing)
        if  singup.email=='' or singup.email=='string' or singup.email.isupper() or not singup.email.endswith('@gmail.com'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='invalid input')
        if  singup.password==''or singup.password=='string':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='invalid input')
        if  singup.name==''or singup.name=='string':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='invalid input')
        new_user=auth(
             name=singup.name,
             email=singup.email,
           password=password,
    lat=singup.lat,
    lan=singup.lan

        )
        self.collection.add(new_user)
        self.collection.commit()
        self.collection.refresh(new_user)

        return new_user
    
    def login_user(self,email:str,password:str):
        user=self.collection.query(auth).filter(auth.email==email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid input')
        unhash_pass=unhash(password,user.password)
        if not unhash_pass:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid password')
        # hotel.is_driver_active = True
        # driver.lat = lat
        # driver.lan = lan
        self.collection.commit()
        self.collection.refresh(user)
        return user