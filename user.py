import mysql.connector

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


def get_user_by_id(user_id): # id ye göre kullanıcı getir 
    connection = mysql.connector.connect(**CONFIG) #veritabanına giriş yapar
    if not connection: # yani veritabanına bağlanamamışsa, ne yapılacağını kontrol eder
        return None
    try: # hata çıkarsa yakala
        cursor=connection.cursor(dictionary=True)
        query="SELECT * FROM food_choice.user WHERE id=%s"# users tablosundan sadece id’si eşleşen kullanıcıyı 
        cursor.execute(query,(user_id,))  # seçer %s kısmı, daha sonra user_id ile doldurulacak ye
        user=cursor.fetchone() # eşleşen bir kullanıcı varsa onu alır
        print(user)
        return user
       
    except Exception as e: # Hata olursa onu e içine kaydet, ben kullanacağım
        print("kullanici getirilemedi")
        print(f"Hata: {e}")
        return None

    finally:
        cursor.close()
        connection.close()
get_user_by_id(29)


def check_is_premium(user_id):
    connection = mysql.connector.connect(**CONFIG) 
    if not connection: 
        return None
    try: 
        cursor=connection.cursor(dictionary=True)
        query="SELECT * FROM food_choice.user WHERE id=%s"
        cursor.execute(query,(user_id,))  
        user=cursor.fetchone()
