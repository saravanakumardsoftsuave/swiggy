from fastapi import APIRouter,Depends,status
from fastapi.security import OAuth2PasswordRequestForm
from user_model.user_model import user_details
from database import get_db
from user_service.user_service import user_service
from user_utils.user_utils import token,get_current
user_route=APIRouter(prefix='/users',tags=['USER'])




@user_route.post('/signup',status_code=status.HTTP_201_CREATED)

def create_user(signup:user_details,db=Depends(get_db)):
    result=user_service(db)
    return  result.create_details(signup)

@user_route.post('/login',status_code=status.HTTP_200_OK)

async def user_login(form_data:OAuth2PasswordRequestForm=Depends(),db=Depends(get_db)):
    login=user_service(db)
    user_login=login.login_user(form_data.username,form_data.password)
    min_token=token({'sub':user_login.email})
    # ref_tok=ref_token({'sub':user_login.driver_name})
    return {
    "access_token": min_token,
    "token_type": "bearer"
}


@user_route.get('/me')
async def current_user(user=Depends(get_current)):
    return{
        'user':user.email
    }


    