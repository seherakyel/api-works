import sys
from fastapi import APIRouter, HTTPException, Request, Form, Response, status
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from functions.company import (create_company,delete_company_by_id,add_company,get_company_by_id,update_company,list_all_company)
from functions.user import user_login
import main  # Ana modülü import ediyoruz (active_user değişkeni için)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

class CompanyBase(BaseModel):
    company_name: str
    description: str
class CompanyCreate(CompanyBase):
    company_id: int 
class CompanyUpdate(BaseModel):
    company_id: int
    company_name: Optional[str] = None
    description: Optional[str] = None


@router.get("/login", response_class=HTMLResponse)
async def show_company_login_page(request: Request):
    return templates.TemplateResponse("company_login.html", {"request": request})

@router.post("/login")
async def handle_company_login(request: Request, user_name: str = Form(...), password: str = Form(...)):
    try:
        print(f"Gelen değerler: user_name={user_name}, password={password}")
        # Önce normal kullanıcıları kontrol edelim
        user = user_login(user_name, password)
        
        if user:
            # Kullanıcı bilgilerini global değişkene kaydedelim
            main.active_user = user
            print(f"Session'a kaydedilen kullanıcı: {user['user_name']}")
            
            # Kullanıcı bulundu, giriş başarılı - ana sayfaya yönlendir
            response = RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)
            return response
        
        # Kullanıcı bulunamadı, hata mesajı göster
        return templates.TemplateResponse("company_login.html", {"request": request, "error": "İşletme adı veya şifre hatalı."})
    except Exception as e:
        print(f"Hata oluştu: {str(e)}")
        return templates.TemplateResponse("company_login.html", {"request": request, "error": f"Giriş hatası: {str(e)}"})

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
