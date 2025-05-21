import sys
from fastapi import APIRouter, HTTPException, Request, Form, Response, status
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from functions.company import (create_company,delete_company_by_id,add_company,get_company_by_id,update_company,list_all_company)
import logging

# Ana modülü artık import etmiyoruz çünkü login işlemlerini main.py'e taşıdık

router = APIRouter()
templates = Jinja2Templates(directory="templates")
logger = logging.getLogger(__name__)

class CompanyBase(BaseModel):
    company_name: str
    description: str
class CompanyCreate(CompanyBase):
    company_id: int 
class CompanyUpdate(BaseModel):
    company_id: int
    company_name: Optional[str] = None
    description: Optional[str] = None

# Kullanıcı login işlemleri main.py'e taşındığı için buradaki login metodlarını kaldırıyoruz

@router.post("/company/create")
async def create_company_endpoint(company: CompanyCreate):
    try:
        logger.info(f"Şirket oluşturma isteği: {company.company_name}")
        create_company(company.company_id, company.company_name, company.description)
        logger.info(f"Şirket oluşturuldu: {company.company_name}")
        return {"message": "sirket oluşturuldu"}
    except Exception as e:
        logger.error(f"Şirket oluşturma hatası: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Hata: {e}")

@router.delete("/company/delete/{company_id}")
async def delete_company_endpoint(company_id: int):
    try:
        logger.info(f"Şirket silme isteği: ID {company_id}")
        delete_company_by_id(company_id)
        logger.info(f"Şirket silindi: ID {company_id}")
        return {"message": f"{company_id} id'li sirket silindi"}
    except Exception as e:
        logger.error(f"Şirket silme hatası: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Hata: {e}")

@router.post("/company/add")
async def add_company_endpoint(company: CompanyBase):
    try:
        logger.info(f"Şirket ekleme isteği: {company.company_name}")
        add_company(company.company_name, company.description)
        logger.info(f"Şirket eklendi: {company.company_name}")
        return {"message": "sirket eklendi"}
    except Exception as e:
        logger.error(f"Şirket ekleme hatası: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Hata: {e}")

@router.get("/company/{company_id}")
async def get_company_endpoint(company_id: int):
    try:
        logger.info(f"Şirket bilgisi isteği: ID {company_id}")
        result = get_company_by_id(company_id)
        return {"company": result}
    except Exception as e:
        logger.error(f"Şirket bilgisi getirme hatası: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Hata: {e}")

@router.put("/company/update")
async def update_company_endpoint(company: CompanyUpdate):
    try:
        logger.info(f"Şirket güncelleme isteği: ID {company.company_id}")
        update_company(
            company_id=company.company_id,
            company_name=company.company_name,
            description=company.description
        )
        logger.info(f"Şirket güncellendi: ID {company.company_id}")
        return {"message": f"{company.company_id} id'li sirket güncellendi"}
    except Exception as e:
        logger.error(f"Şirket güncelleme hatası: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Hata: {e}")

@router.get("/company/all")
async def list_all_company_endpoint():
    try:
        logger.info("Tüm şirketler listesi isteği")
        result = list_all_company()
        return {"companies": result}
    except Exception as e:
        logger.error(f"Şirket listeleme hatası: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Hata: {e}")
