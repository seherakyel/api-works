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


def get_user_by_id(user_id): # id ye göre kullanıcı getir 
    connection = mysql.connector.connect(**CONFIG) #veritabanına giriş yapar
    if not connection: # yani veritabanına bağlanamamışsa, ne yapılacağını kontrol eder
        return None
    try: # hata çıkarsa yakala
        cursor=connection.cursor(dictionary=True)
        query = "SELECT user_name,surname FROM food_choice.user WHERE id=%s"# users tablosundan sadece id'si eşleşen kullanıcıyı 
        cursor.execute(query,(user_id,))  # seçer %s kısmı, daha sonra user_id ile doldurulacak ye
        user=cursor.fetchone() # eşleşen bir kullanıcı varsa onu alır
        return f"{user['user_name']} {user['surname']}"
       
    except Exception as e: # Hata olursa onu e içine kaydet, ben kullanacağım
        print("kullanici getirilemedi")
        print(f"Hata: {e}")
        return None

    finally:
        cursor.close()
        connection.close()
#print(get_user_by_id(2))



def is_premium(user_id):
    connection = mysql.connector.connect(**CONFIG) 
    if not connection: 
        return None
    try: 
        cursor=connection.cursor(dictionary=True)
        query="SELECT * FROM food_choice.user WHERE id=%s"
        cursor.execute(query,(user_id,))  
        user=cursor.fetchone()

        if user and user["is_premium"] == 1:
            print("kullanici premiumludur")
        else:
            print("kullanici premiumlu degildir")

    except Exception as e:
        print(f"hata:{e}")
        return None
    finally:
        cursor.close()
        connection.close()
#(is_premium(2))


def get_user_full_info_by_id(user_id):
    connection=mysql.connector.connect(**CONFIG)
    if not connection:
        return None
    try:
        cursor=connection.cursor(dictionary=True)
        query="SELECT * FROM food_choice.user WHERE id=%s"
        cursor.execute(query,(user_id,))  
        user=cursor.fetchone()
        return user
    
    except Exception as e:
        print("kullanici getirelemedi")
        print(f"hata:{e}")
        return 
    finally:
        cursor.close()
        connection.close()
#print(get_user_full_info_by_id(1))





def user_login(user_name, password):
    try:
        connection = mysql.connector.connect(**CONFIG)
        if not connection:
            print("Veritabanı bağlantısı kurulamadı")
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM user WHERE user_name = %s AND password = %s"
            cursor.execute(query, (user_name, password))
            result = cursor.fetchall()
            if result:
                user = result[0]
                print(f"Giriş başarılı: Hoş geldin {user['user_name']}!")
                return user
            else:
                print("Hatalı kullanıcı adı veya şifre.")
                return None
        except mysql.connector.Error as db_err:
            print(f"Veritabanı işlem hatası: {db_err}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    except mysql.connector.Error as conn_err:
        print(f"Veritabanı bağlantı hatası: {conn_err}")
        return None
    except Exception as e:
        print(f"Beklenmeyen hata: {e}")
        return None



def register_user(user_name, surname, is_premium, age, balance, password):
    connection = mysql.connector.connect(**CONFIG)
    if not connection:
        return None
    try:
        cursor = connection.cursor(dictionary=True)
        # Kullanıcı adı daha önce alınmış mı kontrolü
        cursor.execute("SELECT * FROM user WHERE user_name = %s", (user_name,))
        existing_user = cursor.fetchone()

        if existing_user:
            print(">> Kullanıcı zaten kayıtlı.")
            return False

        # Kayıt işlemi
        cursor.execute("""
            INSERT INTO user(user_name, surname, is_premium, age, balance, password)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (user_name, surname, is_premium, age, balance, password))
        connection.commit()
        print("evet")
        return True

    except Exception as e:
       #print(">> HATA:", e)
        return f"ERROR: {e}"

    finally:
        cursor.close()
        connection.close()
#register_user("a","a",1,20,100,"123")




def delete_user_by_id(user_id):
    connection=mysql.connector.connect(**CONFIG)
    if not connection:
        return None
    try:
        cursor=connection.cursor(dictionary=True)
        query="DELETE FROM user WHERE id=%s"
        cursor.execute(query,(user_id,))
        connection.commit()
        print(f"{user_id} kullanicisi silindi")

    except Exception as e:
        print("kullanici silenemedi")
        print(f"hata:{e}")
        return None
    
    finally:
        cursor.close()
        connection.close()
#print(delete_user_by_id(13))



def list_all_users():
    connection = mysql.connector.connect(**CONFIG) #veritabanına giriş yapar
    if not connection: # yani veritabanına bağlanamamışsa, ne yapılacağını kontrol eder
        return None
    try: # hata çıkarsa yakala
        cursor=connection.cursor(dictionary=True)
        query = "SELECT*FROM food_choice.user"# users tablosundan tüm kullanıcıyı görüntüle
        cursor.execute(query,)
        return cursor.fetchall() #tüm kullanıcıları toplar

    except Exception as e:
        print("kullanici listelenmedi")
        print(f"hata:{e}")
        return None
    finally:
        cursor.close()
        connection.close()
#print(list_all_users())

#connection.commit() "veritabanındaki değişiklikleri kaydet" anlamına gelir ve sadece INSERT, UPDATE, DELETE gibi işlemlerden sonra kullanılır SELECTte kullanılmaz


def update_user(user_id, user_name, surname, is_premium, age, balance, password):
    connection = mysql.connector.connect(**CONFIG)
    try:
        cursor = connection.cursor()
        query = """
        UPDATE user SET
            user_name = %s,
            surname = %s,
            is_premium = %s,
            age = %s,
            balance = %s,
            password = %s
        WHERE id = %s
        """
        values = (user_name, surname, is_premium, age, balance, password, user_id)
        cursor.execute(query, values)
        connection.commit()  
        print("kullanıcı güncellendi")
    except Exception as e:
        print("güncelleme hatası:", e)
    finally:
        cursor.close()
        connection.close()

#print(sonuc)


        
    


