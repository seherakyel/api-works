import sys
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from functions.user import (
    add_user, get_user_by_id, delete_user_by_id, is_premium, get_user_full_info_by_id, update_user,list_all_users
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
    


@router.get("/is_premium/{user_id}")
async def is_premium_endpoint(user_id: int):
    try:
        is_premium(user_id)
        return {"message": "Premium durumu kontrol edildi"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hata: {str(e)}")



@router.get("/get_user/{user_id}")
async def get_user_endpoint(user_id: int):
    try:
        user = get_user_full_info_by_id(user_id)
        if user:
            return {"message": "Kullanıcı bulundu", "data": user}
        else:
            return {"message": "Kullanıcı bulunamadı", "data": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hata: {str(e)}")
    

class UpdateUser(BaseModel):
    user_id: int
    user_name: Optional[str] = None
    surname: Optional[str] = None
    is_premium: Optional[int] = None
    age: Optional[int] = None
    balance: Optional[int] = None

@router.put("/update_user") # PUT isteği: Var olan kullanıcıyı güncellemek için kullanılır
async def update_user_endpoint(user: UpdateUser): # Gelen veri, UpdateUser modeline göre kontrol edilir
    try:
        update_user(
            user_id=user.user_id, # Gelen veri, UpdateUser modeline göre kontrol edilir
            user_name=user.user_name, # Yeni ad (gönderildiyse)
            surname=user.surname, # Yeni ad (gönderildiyse)
            is_premium=user.is_premium, # Premium durumu (1 veya 0)
            age=user.age, # Yeni yaş bilgisi
            balance=user.balance  # Yeni bakiye bilgisi
        )
        return {"message": "Kullanıcı güncellendi"} # İşlem başarılıysa bu mesaj dönülür
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hata: {str(e)}")




@router.get("/list_users")
async def list_all_users_endpoint(user:list):
    try:
        list_all_users()
        return {"message":"kullanici listesi olusturuldu"}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="kullanici listesi olusturulmadi")

