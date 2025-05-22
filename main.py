from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import logging
import traceback  # Hata izleme için eklenmiştir
import random

from routes.user_routes import router as user_routes
from routes.food_routes import router as food_routes
from routes.order_routes import router as order_routes
from routes.owner_routes import router as owner_routes
from routes.company_routes import router as company_routes

from functions.user import register_user, user_login
from functions.food import list_all_foods

# Aktif kullanıcı için basit bir session oluşturuyoruz
# Gerçek uygulamada daha güvenli bir session yönetimi kullanılmalıdır
active_user = {}
# Kullanıcı tipini (user veya business) izleme
user_type = ""

# Loglama yapılandırması
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# İşletme Giriş sayfası için endpoint
@app.get("/", response_class=HTMLResponse)
async def redirect_to_login(request: Request):
    # Ana sayfadan kullanıcı girişine yönlendir
    logger.info("Ana sayfa isteği, kullanıcı girişine yönlendiriliyor")
    return RedirectResponse(url="/user/login", status_code=303)

@app.get("/business/login", response_class=HTMLResponse)
async def show_business_login_page(request: Request):
    logger.info("İşletme giriş sayfası görüntüleniyor")
    return templates.TemplateResponse("login.html", {"request": request})

# İşletme girişi işlemi
@app.post("/business/login")
async def handle_business_login(request: Request, user_name: str = Form(...), password: str = Form(...)):
    global active_user, user_type
    logger.info(f"İşletme girişi denemesi: {user_name}")
    
    user = user_login(user_name, password)
    if user:
        # İşletme girişi olduğunu işaretle
        active_user = user
        user_type = "business"
        logger.info(f"İşletme girişi başarılı: {user_name}")
        
        # İşletme ana sayfasına yönlendir
        return RedirectResponse(url="/business/home", status_code=303)
    else:
        logger.warning(f"İşletme girişi başarısız: {user_name}")
        return templates.TemplateResponse("login.html", {"request": request, "error": "İşletme adı veya şifre hatalı."})

@app.get("/register", response_class=HTMLResponse)
async def show_register_page(request: Request):
    logger.info("Kayıt sayfası görüntüleniyor")
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register", response_class=HTMLResponse)
async def handle_register(request: Request, user_name: str = Form(...), surname: str = Form(...), is_premium: int = Form(...), age: int = Form(...), balance: int = Form(...), password: str = Form(...)):
    logger.info(f"Kayıt denemesi: {user_name}")
    user = register_user(user_name, surname, is_premium, age, balance, password)
    if user:
        logger.info(f"Kayıt başarılı: {user_name}")
        # Kullanıcı kaydı başarılı olduğunda, kullanıcı giriş sayfasına yönlendir
        return RedirectResponse(url="/user/login?success=true&username=" + user_name, status_code=303)
    
    logger.warning(f"Kayıt başarısız: {user_name}")
    return templates.TemplateResponse("register.html", {"request": request, "Hata": "Kayıt başarısız"})

@app.get("/user/login", response_class=HTMLResponse)
async def show_user_login_page(request: Request):
    # URL'den parametreleri al
    success = request.query_params.get("success", "")
    username = request.query_params.get("username", "")
    
    logger.info("Kullanıcı giriş sayfası görüntüleniyor")
    
    # Başarılı kayıt durumunda başarı mesajı göster
    if success == "true" and username:
        logger.info(f"Başarılı kayıt mesajı gösteriliyor: {username}")
        return templates.TemplateResponse("company_login.html", {
            "request": request, 
            "success": f"{username} başarıyla kayıt oldu."
        })
    
    return templates.TemplateResponse("company_login.html", {"request": request})

@app.post("/user/login")
async def handle_user_login(request: Request, user_name: str = Form(...), password: str = Form(...)):
    global active_user, user_type
    logger.info(f"Kullanıcı girişi denemesi: {user_name}")
    
    try:
        # Önce normal kullanıcıları kontrol edelim
        user = user_login(user_name, password)
        
        if user:
            # Kullanıcı bilgilerini global değişkene kaydedelim
            active_user = user
            # Normal kullanıcı girişi olduğunu belirtelim
            user_type = "user"
            logger.info(f"Kullanıcı girişi başarılı: {user_name}")
            
            # Kullanıcı bulundu, giriş başarılı - kullanıcı ana sayfasına yönlendir
            return RedirectResponse(url="/home", status_code=303)
        
        # Kullanıcı bulunamadı, hata mesajı göster
        logger.warning(f"Kullanıcı girişi başarısız: {user_name}")
        return templates.TemplateResponse("company_login.html", {"request": request, "error": "Kullanıcı adı veya şifre hatalı."})
    except Exception as e:
        # Hata detaylarını loglayalım
        error_details = traceback.format_exc()
        logger.error(f"Kullanıcı girişi hatası: {str(e)}")
        logger.debug(f"Hata detayları: {error_details}")
        
        # Kullanıcıya anlamlı bir hata mesajı gösterelim
        return templates.TemplateResponse("company_login.html", {"request": request, "error": "Giriş sırasında bir hata oluştu. Lütfen daha sonra tekrar deneyin."})

@app.get("/foods", response_class=HTMLResponse)
async def show_foods_page(request: Request):
    logger.info("Yemekler sayfası görüntüleniyor")
    return templates.TemplateResponse("foods.html", {"request": request})

# Kullanıcı profil sayfası
@app.get("/profile", response_class=HTMLResponse)
async def show_profile_page(request: Request):
    # Global değişkenden kullanıcı bilgisini alalım
    user = active_user
    # Eğer kullanıcı bilgisi yoksa kullanıcı girişine yönlendir
    if not user:
        logger.warning("Profil sayfası erişim denemesi: Kullanıcı oturumu bulunamadı")
        return RedirectResponse(url="/user/login", status_code=303)
    
    logger.info(f"Kullanıcı profil sayfası gösteriliyor: {user.get('user_name', 'Bilinmiyor')}")
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})

# İşletme profil sayfası
@app.get("/business/profile", response_class=HTMLResponse)
async def show_business_profile_page(request: Request):
    # Global değişkenden kullanıcı bilgisini alalım
    user = active_user
    # Eğer kullanıcı bilgisi yoksa işletme girişine yönlendir
    if not user:
        logger.warning("İşletme profil sayfası erişim denemesi: Kullanıcı oturumu bulunamadı")
        return RedirectResponse(url="/business/login", status_code=303)
    # Kullanıcı türü işletme değilse işletme home'a yönlendir
    elif user_type != "business":
        logger.warning(f"İşletme profil sayfası erişim denemesi: Yanlış kullanıcı türü ({user_type})")
        return RedirectResponse(url="/home", status_code=303)
    
    logger.info(f"İşletme profil sayfası gösteriliyor: {user.get('user_name', 'Bilinmiyor')}")
    return templates.TemplateResponse("business_profile.html", {"request": request, "user": user})

# Kullanıcı ana sayfası
@app.get("/home", response_class=HTMLResponse)
async def show_home_page(request: Request):
    # Global değişkenden kullanıcı bilgisini alalım
    user = active_user
    # Eğer kullanıcı bilgisi yoksa varsayılan gönderelim
    if not user:
        logger.warning("Kullanıcı oturumu bulunamadı, varsayılan değerler kullanılıyor")
        user = {"user_name": "Misafir", "balance": 0}
    elif user_type != "user":
        # Kullanıcı türü normal kullanıcı değilse işletme ana sayfasına yönlendir
        logger.info(f"Kullanıcı türü uyumsuz: {user_type}, işletme sayfasına yönlendiriliyor")
        return RedirectResponse(url="/business/home", status_code=303)
    
    try:
        logger.info(f"Kullanıcı ana sayfası gösteriliyor: {user.get('user_name', 'Bilinmiyor')}")
        return templates.TemplateResponse("home.html", {"request": request, "user": user})
    except Exception as e:
        # Hata detaylarını loglayalım
        error_details = traceback.format_exc()
        logger.error(f"Ana sayfa gösterilirken hata: {str(e)}")
        logger.debug(f"Hata detayları: {error_details}")
        
        # Kullanıcıya anlamlı bir hata mesajı gösterelim
        return templates.TemplateResponse("error.html", {
            "request": request, 
            "error_title": "Sayfa Görüntülenemedi",
            "error_message": "Ana sayfa yüklenirken bir hata oluştu. Lütfen daha sonra tekrar deneyin."
        })

@app.get("/business/home", response_class=HTMLResponse)
async def show_business_home(request: Request):
    # Global değişkenden kullanıcı bilgisini alalım
    user = active_user
    # Eğer kullanıcı bilgisi yoksa varsayılan gönderelim
    if not user:
        logger.warning("İşletme oturumu bulunamadı, varsayılan değerler kullanılıyor")
        user = {"user_name": "İşletme Sahibi", "balance": 0}
    elif user_type != "business":
        # Kullanıcı türü işletme değilse ana sayfaya yönlendir
        logger.info(f"Kullanıcı türü uyumsuz: {user_type}, kullanıcı sayfasına yönlendiriliyor")
        return RedirectResponse(url="/home", status_code=303)
    
    logger.info(f"İşletme ana sayfası gösteriliyor: {user.get('user_name', 'Bilinmiyor')}")
    return templates.TemplateResponse("business_home.html", {"request": request, "user": user})

# Mevcut router'lar
# Birincil (öncelikli) rotaları kendimiz tanımladık. Diğer endpoint'ler için router'ları include ediyoruz
app.include_router(user_routes, prefix="/users", tags=["Users"])
app.include_router(food_routes, prefix="/foods", tags=["Foods"])
app.include_router(order_routes, prefix="/orders", tags=["Orders"])
app.include_router(owner_routes, prefix="/owners", tags=["Owners"])
app.include_router(company_routes, tags=["Company"])

@app.get("/logout")
async def logout(request: Request):
    # Oturumu temizle
    global active_user, user_type
    active_user = {}
    user_type = ""
    logger.info("Kullanıcı çıkış yaptı")
    # Ana sayfaya yönlendir (ana sayfa zaten login'e yönlendiriyor)
    return RedirectResponse(url="/", status_code=303)

# API endpoint: Rastgele yemek getir
@app.get("/api/random-food", response_class=JSONResponse)
async def get_random_food():
    try:
        # Tüm yemekleri getir
        foods = list_all_foods()
        
        if not foods or len(foods) == 0:
            # Eğer veritabanında yemek yoksa örnek veri döndür
            logger.warning("Veritabanında yemek bulunamadı, örnek veri gönderiliyor")
            sample_foods = [
                {"food_name": "Karışık Pizza", "description": "İtalyan usulü hazırlanan, özel peynir karışımı ve taze malzemelerle süslenmiş lezzetli pizza.", "price": 120},
                {"food_name": "Deluxe Burger", "description": "%100 dana eti, özel soslar, taze sebzeler ve özel ekmeği ile enfes bir burger deneyimi.", "price": 95},
                {"food_name": "Adana Kebap", "description": "Geleneksel baharatlarla harmanlanmış, ızgarada ustalıkla pişirilmiş Adana kebap.", "price": 130},
                {"food_name": "Tavuk Döner", "description": "Özel marine edilmiş tavuk eti, taze sebzeler ve özel sosla servis edilen lezzetli döner.", "price": 75},
                {"food_name": "İzmir Köfte", "description": "Özel baharatlarla hazırlanmış, yanında patates ve sebzelerle servis edilen nefis köfte.", "price": 110}
            ]
            random_food = random.choice(sample_foods)
            return random_food
        
        # Rastgele bir yemek seç
        random_food = random.choice(foods)
        
        # Description alanı database'de yoksa, ekliyoruz
        if "description" not in random_food:
            food_descriptions = {
                "Margherita Pizza": "İtalyan mutfağının klasiği, mozarella peyniri ve taze fesleğen yaprakları ile.",
                "Pepperoni Pizza": "Bol baharatlı pepperoni dilimleri ile zenginleştirilmiş nefis bir pizza.",
                "Cheeseburger": "Özel soslar ve erimiş peynir ile hazırlanan lezzetli bir hamburger.",
                "Tavuk Burger": "Marine edilmiş tavuk göğsü ile hazırlanmış, hafif ve lezzetli bir seçenek."
            }
            random_food["description"] = food_descriptions.get(random_food["food_name"], "Özel tarifle hazırlanmış lezzetli bir seçim.")
        
        # Veriyi döndür
        formatted_food = {
            "food_name": random_food["food_name"],
            "description": random_food.get("description", "Lezzetli bir tercih!"),
            "price": random_food["price"]
        }
        
        logger.info(f"Rastgele yemek gönderildi: {formatted_food['food_name']}")
        return formatted_food
        
    except Exception as e:
        logger.error(f"Rastgele yemek API hatası: {str(e)}")
        # Hata durumunda varsayılan bir yemek gönder
        return {
            "food_name": "Günün Menüsü",
            "description": "Şu anda menü bilgisi alınamadı. Lütfen daha sonra tekrar deneyin.",
            "price": 99
        }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)



