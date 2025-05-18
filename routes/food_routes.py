

import sys
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from functions.food import (
    add_food, get_food_by_id, delete_food_by_id, get_food_full_info_by_id, update_food,list_all_foods
)

router = APIRouter()
class AddFood (BaseModel):
    food_name: str
    stock: int
    price: int
    distance: float    

@router.post("/add")
async def add_food_endpoint(food: AddFood):
    try:
        add_food(
            food.food_name,
            food.stock,
            food.price,
            food.distance   
        )
        return {"message": True}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="yemek eklenmedi")


@router.get("/food/{food_id}")
async def get_food_by_id_endpoint(food_id: int):
    try:
        food = get_food_by_id(food_id)
        if food:
            return {"message": "food found", "food": food, "status": 200}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="yemek getirelemedi")



@router.delete("/delete/{food_id}")
async def delete_food_by_id_enpoint(food_id: int):
    try:
        delete_food_by_id(food_id)
        return {"message": "User deleted"}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="kullanici silinmedi.")
    

@router.get("/get_user/{food_id}")
async def get_food_endpoint(food_id: int):
    try:
        food = get_food_full_info_by_id(food_id)
        if food:
            return {"message": "yemek bulundu", "data": food}
        else:
            return {"message": "yemek bulunamadı", "data": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hata: {str(e)}")
    

class UpdateUser(BaseModel):
    food_id: int
    food_name: Optional[str] = None
    stock: Optional[int] = None
    price: Optional[int] = None
    distance: Optional[float] = None
 

@router.put("/update_food") # PUT isteği: Var olan kullanıcıyı güncellemek için kullanılır
async def update_food_endpoint(food: update_food): # Gelen veri, UpdateUser modeline göre kontrol edilir
    try:
        update_food(
            food_id=food.food_id, # Gelen veri, UpdateUser modeline göre kontrol edilir
            food_name=food.food_name, # Yeni ad (gönderildiyse)
            stock=food.stock, # Yeni stok (gönderildiyse)
            price=food.iprice, # yeni fiyat
            distance=food.distance, # Yeni mesafe bilgisi
           
        )
        return {"message": " yemek güncellendi"} # İşlem başarılıysa bu mesaj dönülür
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hata: {str(e)}")
    



@router.get("/list_food")
async def list_all_foods_endpoint(food:list):
    try:
        list_all_foods()
        return {"message":"yemek listesi olusturuldu"}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="yemek listesi olusturulmadi")

        




