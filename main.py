from fastapi import FastAPI
from routes.user_routes import router as user_routes # from klasöradı.dosyaadı import router(yani bunu router olarak kaydet diyoruz) as x (yani takma adı)
from routes.food_routes import router as food_routes
app = FastAPI()

app.include_router(user_routes, prefix="/users", tags=["Users"])
app.include_router(food_routes,prefix="/foods",tags=["Foods"])