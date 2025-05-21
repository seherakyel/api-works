from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from routes.user_routes import router as user_routes
from routes.food_routes import router as food_routes
from routes.order_routes import router as order_routes
from routes.owner_routes import router as owner_routes
from routes.company_routes import router as company_routes


from functions.user import register_user, user_login

# Aktif kullanıcı için basit bir session oluşturuyoruz
# Gerçek uygulamada daha güvenli bir session yönetimi kullanılmalıdır
active_user = {}

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
        return templates.TemplateResponse("company_login.html", {"request": request, "success": f"{user_name} başarıyla kayıt oldu."})
    return templates.TemplateResponse("register.html", {"request": request, "Hata": "Kayıt başarısız"})




from routes.food_routes import router as food_router

app.include_router(food_router)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/foods", response_class=HTMLResponse)
async def show_foods_page(request: Request):
    return templates.TemplateResponse("foods.html", {"request": request})

@app.get("/home", response_class=HTMLResponse)
async def show_home_page(request: Request):
    # Global değişkenden kullanıcı bilgisini alalım
    user = active_user
    # Eğer kullanıcı bilgisi yoksa varsayılan gönderelim
    if not user:
        user = {"user_name": "Misafir", "balance": 0}
    
    print(f"Ana sayfa için kullanıcı: {user.get('user_name', 'Bilinmiyor')}")
    return templates.TemplateResponse("home.html", {"request": request, "user": user})


# Mevcut router'lar
# İşletme routerlarını özellikle prefix kullanmadan dahil ediyoruz 
# Böylece '/company/login' ve benzeri URL'ler doğrudan çalışacak
app.include_router(company_routes, tags=["Company"])

app.include_router(user_routes, prefix="/users", tags=["Users"])
app.include_router(food_routes, prefix="/foods", tags=["Foods"])
app.include_router(order_routes, prefix="/orders", tags=["Orders"])
app.include_router(owner_routes, prefix="/owners", tags=["Owners"])

# Eski company router'ı kaldırıldı (prefix="/company" ile olan)

@app.get("/logout")
async def logout(request: Request):
    # Oturumu temizle
    global active_user
    active_user = {}
    # Ana sayfaya yönlendir
    return RedirectResponse(url="/", status_code=303)



