import sys
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.users import (
    add_user, get_user_by_id,delete_user_by_id, # check_is_premium,get_user_full_info_by_id,update_user
)
router = APIRouter()
class RegisterUser(BaseModel):
    user_name: str
    surname: str
    is_premium: str
    age: int
    balance: str



@router.post("/add")
async def add_user_endpoint(user: RegisterUser):
    try:
        add_user(
            user.user_name,
            user.surname,
            user.is_premium,
            user.age,
            user.balance
        )
        return {"message": True}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="kullanici eklenmedi")

@router.get("/user/{user_id}")
async def get_user_by_id_endpoint(user_id: int):
    try:
        user = get_user_by_id(user_id)
        if user:
            return {"message": "User found", "user": user, "status": 200}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="kullanici getirelemedi")



@router.delete("/delete/{user_id}")
async def delete_user_by_id_enpoint(user_id: int):
    try:
        delete_user_by_id(user_id)
        return {"message": "User deleted"}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="kullanici silinmedi.")


