from fastapi import FastAPI
from routes.user_routes import router as user_routes # from klasöradı.dosyaadı import router(yani bunu router olarak kaydet diyoruz) as x (yani takma adı)
from routes.food_routes import router as food_routes
from routes.order_routes import router as order_routes
from routes.owner_routes import router as owner_routes
from routes.company_routes import router as company_routes
app = FastAPI()

app.include_router(user_routes, prefix="/users", tags=["Users"])
app.include_router(food_routes,prefix="/foods",tags=["Foods"])
app.include_router(order_routes,prefix="/orders",tags=["Orders"])
app.include_router(owner_routes,prefix="/owners",tags=["Owners"])
app.include_router(company_routes,prefix="/company",tags=["Company"])