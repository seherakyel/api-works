import sys
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from functions.owner import ( login_owner,delete_owner_by_id,add_owner, get_owner_by_id,update_owner,list_all_owner
                             
)

router = APIRouter()

class OwnerBase(BaseModel):
    mail: str
    password: str
class OwnerLogin(OwnerBase):
    owner_id: int
class OwnerUpdate(BaseModel):
    owner_id: int
    mail: Optional[str] = None
    password: Optional[str] = None
class OwnerID(BaseModel):
    owner_id: int

@router.post("/owner/login")
async def login_owner_endpoint(owner: OwnerLogin):
    try:
        login_owner(owner.owner_id, owner.mail, owner.password)
        return {"message": "isletme olusturuldu"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"olusturulmadi: {e}")
    


@router.delete("/owner/delete/{owner_id}")
async def delete_owner_endpoint(owner_id: int):
    try:
        delete_owner_by_id(owner_id)
        return {"message": f"{owner_id} id'li isletme silindi"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"silinmedi: {e}")




@router.post("/owner/add")
async def add_owner_endpoint(owner: OwnerBase):
    try:
        result = add_owner(owner.mail, owner.password)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"eklenmedi: {e}")





@router.get("/owner/{owner_id}")
async def get_owner_endpoint(owner_id: int):
    try:
        result = get_owner_by_id(owner_id)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"getirilemedi: {e}")




@router.put("/owner/update")
async def update_owner_endpoint(owner: OwnerUpdate):
    try:
        update_owner(
            owner_id=owner.owner_id,
            mail=owner.mail,
            password=owner.password
        )
        return {"message": f"{owner.owner_id} güncellendi"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"guncellenmedi: {e}")





@router.get("/owner/all")
async def list_all_owner_endpoint():
    try:
        result = list_all_owner()
        return {"owners": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"listelenmedi: {e}")

