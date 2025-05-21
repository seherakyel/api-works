from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from routes.user_routes import router as user_routes
from routes.food_routes import router as food_routes
from routes.order_routes import router as order_routes
from routes.owner_routes import router as owner_routes
from routes.company_routes import router as company_routes


from functions.user import register_user, user_login

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Giriş sayfası için endpoint
@app.get("/", response_class=HTMLResponse)
async def show_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


templates = Jinja2Templates(directory="templates")


@app.post("/login", response_class=HTMLResponse)
async def handle_login(request: Request, user_name: str = Form(...), password: str = Form(...)):

    user = user_login(user_name, password)
    if user:
        return templates.TemplateResponse("home.html", {"request": request, "user": user})
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Kullanıcı adı veya şifre hatalı."})


@app.get("/register", response_class=HTMLResponse)
async def show_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register", response_class=HTMLResponse)
async def show_register_page(request: Request, user_name: str = Form(...), surname: str = Form(...), is_premium: int = Form(...), age: int = Form(...), balance: int = Form(...), password: str = Form(...)):

    user = register_user(user_name,surname, is_premium, age,balance, password)
    if user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Kullanıcı adı veya şifre hatalı."})
    return templates.TemplateResponse("register.html", {"request": request, "Hata": "Kayıt başarısız"})



# Mevcut router'lar
app.include_router(user_routes, prefix="/users", tags=["Users"])
app.include_router(food_routes, prefix="/foods", tags=["Foods"])
app.include_router(order_routes, prefix="/orders", tags=["Orders"])
app.include_router(owner_routes, prefix="/owners", tags=["Owners"])
app.include_router(company_routes, prefix="/company", tags=["Company"])
app.include_router(user_routes, prefix="/users", tags=["Users"])

