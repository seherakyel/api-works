import sys
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from functions.company import (create_company,delete_company_by_id,add_company,get_company_by_id,update_company,list_all_company)

router = APIRouter()

class CompanyBase(BaseModel):
    company_name: str
    description: str
class CompanyCreate(CompanyBase):
    company_id: int 
class CompanyUpdate(BaseModel):
    company_id: int
    company_name: Optional[str] = None
    description: Optional[str] = None



@router.post("/company/create")
async def create_company_endpoint(company: CompanyCreate):
    try:
        create_company(company.company_id, company.company_name, company.description)
        return {"message": "sirket oluşturuldu"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hata: {e}")




@router.delete("/company/delete/{company_id}")
async def delete_company_endpoint(company_id: int):
    try:
        delete_company_by_id(company_id)
        return {"message": f"{company_id} id'li sirket silindi"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hata: {e}")




@router.post("/company/add")
async def add_company_endpoint(company: CompanyBase):
    try:
        add_company(company.company_name, company.description)
        return {"message": "sirket eklendi"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hata: {e}")




@router.get("/company/{company_id}")
async def get_company_endpoint(company_id: int):
    try:
        result = get_company_by_id(company_id)
        return {"company": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hata: {e}")




@router.put("/company/update")
async def update_company_endpoint(company: CompanyUpdate):
    try:
        update_company(
            company_id=company.company_id,
            company_name=company.company_name,
            description=company.description
        )
        return {"message": f"{company.company_id} id'li sirket güncellendi"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hata: {e}")




@router.get("/company/all")
async def list_all_company_endpoint():
    try:
        result = list_all_company()
        return {"companies": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hata: {e}")
