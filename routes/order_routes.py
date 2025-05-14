from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from functions.order import (
    get_order_by_id,add_order,delete_order_by_id,update_order
)

router = APIRouter()
class AddOrder (BaseModel):
    user_id:int
    food_id:int
    order_status:str
    order_payment:str
    order_time:int


@router.post("/add")
async def add_order_enpoint(order:AddOrder):
    try:
        add_order(
            order.user_id,
            order.food_id,
            order.order_status,
            order.order_payment,
            order.order_time
        )
        return {"message ": True}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except ValueError as e:
        raise HTTPException(status_code=500, detail="yemek eklenmedi")
    

@router.get("/order/{order_id}")
async def get_order_by_id_endpoint(order_id: int): #İstenen siparişi (order) id’sine göre getirir.
    try:
        order = get_order_by_id(order_id)
        if order: # order boş değilse cevabı döndür
            return {"message": "order found", "order": order, "status": 200}
        raise HTTPException(status_code=404, detail="order not found") # order None veya [] geldiyse 404 fırlatalım

    except ValueError as ve: # id negatif vb. özel hatalar
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception:  # beklenmeyen her şey
        raise HTTPException(status_code=500, detail="sipariş getirilemedi")
    

@router.delete("/delete/{order_id}")
async def delete_order_by_id_enpoint(order_id: int):
    try:
        deleted = delete_order_by_id(order_id)  
        if deleted:
            return {"message": "order deleted", "status": 200}
        raise HTTPException(status_code=404, detail="order not found")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception:
        raise HTTPException(status_code=500, detail="sipariş silinemedi")
    

# Güncelleme isteğinde yalnızca değişecek alanları göndereceğiz; bu
# yüzden hepsi Optional. order_id URL’den, diğer alanlar body’den gelir
class UpdateOrder(BaseModel):
    user_id:      Optional[int]  = None
    food_id:      Optional[int]  = None
    order_status: Optional[str]  = None
    order_payment:Optional[str]  = None
    order_time:   Optional[int]  = None   # datetime tercih edebilirsin

@router.put("/{order_id}")
async def update_order_by_id_endpoint(order_id: int, order: UpdateOrder):
    try:
        # update_order fonksiyonuna id ve güncellenebilir alanlar
        updated = update_order(
            order_id       = order_id,
            user_id        = order.user_id,
            food_id        = order.food_id,
            order_status   = order.order_status,
            order_payment  = order.order_payment,
            order_time     = order.order_time,
        )

        if updated:
            return {"message": "order updated", "status": 200}
        raise HTTPException(status_code=404, detail="order not found")

    except ValueError as ve: # örn. tip hataları
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception: # beklenmeyen hatalar
        raise HTTPException(status_code=500, detail="sipariş güncellenemedi")

    








    





