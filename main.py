from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from routes.user_routes import router as user_routes
from routes.food_routes import router as food_routes
from routes.order_routes import router as order_routes
from routes.owner_routes import router as owner_routes
from routes.company_routes import router as company_routes

app = FastAPI()

# Statik dosyaları tanıt (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# HTML şablonlarını tanıt (login.html burada olacak)
templates = Jinja2Templates(directory="templates")

# Giriş sayfası için endpoint
@app.get("/", response_class=HTMLResponse)
async def show_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Mevcut router'lar
app.include_router(user_routes, prefix="/users", tags=["Users"])
app.include_router(food_routes, prefix="/foods", tags=["Foods"])
app.include_router(order_routes, prefix="/orders", tags=["Orders"])
app.include_router(owner_routes, prefix="/owners", tags=["Owners"])
app.include_router(company_routes, prefix="/company", tags=["Company"])
