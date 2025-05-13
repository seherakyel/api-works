import mysql.connector
from mysql.connector import Error

CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456789',
    'database': 'food_choice'
}
def is_db_connected():
    connection = mysql.connector.connect(**CONFIG)
    if not connection:
        print("Bağlantı başarısız")
    else:
        print("Bağlantı başarılı")

is_db_connected()

def get_food_by_id(food_id): # belirli id ye göre yemke getirir
    connection=mysql.connector.connect(**CONFIG) # veritabanına bağlanır 
    if not connection: # bağlantı başarısızsa 
        return None # hiçbir şey döndürmez
    try:
        cursor=connection.cursor(dictionary=True) # yemek tablosunu sözlük olarak getirir
        query = "SELECT food_name FROM food_choice.food WHERE id=%s" # belirli id li yemeği seçen sql sorgusu 
        cursor.execute(query,(food_id,))  # sorguyu çalıştırır %s yerine food_id  gelir
        user=cursor.fetchone() # eşleşen bir kullanıcı varsa onu alır
        return f"{user['food_name']}" # elde edilen yemeğin adsını döndürür
    
    except Exception as e: # eğer hata olursa hatayı e nin içine kaydet 
        print("yemek getirilemedi") # hata mesajı yazdırlır 
        print(f"hata:{e}") # hatanın kendisini yazdırılır
        return None 
    finally:
        cursor.close() # cursor kapatılır
        connection.close() # veritabanı bağlantısı kapatılır
print(get_food_by_id(28)) # idsi 28 olan yemeğin adını yazdırır


    

