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
        query = "SELECT user_name,surname FROM food_choice.user WHERE id=%s"# users tablosundan sadece id’si eşleşen kullanıcıyı 
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
print(get_user_by_id(29))



def check_is_premium(user_id):
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
check_is_premium(30)


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
print(get_user_full_info_by_id(29))

def add_user(user_name,surname,is_premium,age,balance):
    connection=mysql.connector.connect(**CONFIG)
    if not connection:
        return None
    try:
        cursor = connection.cursor(dictionary=True)
        query="INSERT INTO user(user_name,surname,is_premium,age,balance) VALUES(%s,%s,%s,%s,%s)"
        cursor.execute(query,(user_name,surname,is_premium,age,balance))
        connection.commit()
        print(f"{ user_name} kullanicisi eklendi")
    except Exception as e:
        print("kullanici eklenmedi")
        print(f"hata:{e}")
    finally:
        cursor.close()
        connection.close()
print(add_user("seher","akyel",1,20,560))


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
print(delete_user_by_id(29))

