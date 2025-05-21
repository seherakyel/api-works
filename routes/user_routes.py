import sys
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from functions.user import (
     user_login,register_user,get_user_by_id, delete_user_by_id, is_premium, get_user_full_info_by_id, update_user,list_all_users
)



class RegisterUser(BaseModel):
    user_name: str
    surname: str
    is_premium: int
    age: int
    balance: int
    password: str



class UpdateUser(BaseModel):
    user_id: int
    user_name: Optional[str] = None
    surname: Optional[str] = None
    is_premium: Optional[int] = None
    age: Optional[int] = None
    balance: Optional[int] = None
    password:Optional[str] = None

router = APIRouter()

@router.post("/login")
async def user_login_endpoint(user_name: str, password: str):
    user = user_login(user_name, password)
    if user:
        return {"message": f"Giriş başarılı: Hoş geldin {user['user_name']}", "user": user}
    else:
        raise HTTPException(status_code=401, detail="Kullanıcı adı veya şifre hatalı.")
    

@router.post("/register")
async def user_register_endpoint(user: RegisterUser):
    result = register_user(user.user_name, user.surname, user.is_premium, user.age, user.balance, user.password)
    if result:
        return JSONResponse(content={"message": f"{user.user_name} başarıyla kayıt oldu."})
    else:
        raise HTTPException(status_code=400, detail="Kayıt işlemi başarısız. Kullanıcı adı alınmış olabilir.")




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
    


@router.put("/update_user") # PUT isteği: Var olan kullanıcıyı güncellemek için kullanılır
async def update_user_endpoint(user: UpdateUser): # Gelen veri, UpdateUser modeline göre kontrol edilir
    try:
        update_user(
            user_id=user.user_id, # Gelen veri, UpdateUser modeline göre kontrol edilir
            user_name=user.user_name, # Yeni ad (gönderildiyse)
            surname=user.surname, # Yeni ad (gönderildiyse)
            is_premium=user.is_premium, # Premium durumu (1 veya 0)
            age=user.age, # Yeni yaş bilgisi
            balance=user.balance, # Yeni bakiye bilgisi
            password=user.password
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

