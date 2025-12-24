from fastapi import APIRouter,Depends,status
from fastapi.security import OAuth2PasswordRequestForm
from hotel_model.hotel_model import hotel_details
from database import get_db
from hotel_service.hotel_service import hotel_service
from hotel_utils.hotel_utils import token,get_current
hotel_route=APIRouter(prefix='/hotel',tags=['HOTEL'])




@hotel_route.post('/signup',status_code=status.HTTP_201_CREATED)

def create_driver(signup:hotel_details,db=Depends(get_db)):
    result=hotel_service(db)
    return  result.create_details(signup)

@hotel_route.post('/login',status_code=status.HTTP_200_OK)

async def login(form_data:OAuth2PasswordRequestForm=Depends(),db=Depends(get_db)):
    login=hotel_service(db)
    user_login=login.login_hotel(form_data.username,form_data.password)
    min_token=token({'sub':user_login.email})
    # ref_tok=ref_token({'sub':user_login.driver_name})
    return {
    "access_token": min_token,
    "token_type": "bearer"
}


@hotel_route.get('/me')
async def current_user(user=Depends(get_current)):
    return{
        'user':user.email
    }


    