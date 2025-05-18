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
is_premium(30)


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
#print(get_user_full_info_by_id(29))

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
#print(add_user("seher","akyel",1,20,560))


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


def update_user(user_id,user_name=None,surname=None,is_premium=None,age=None,balance=None):
    connection=mysql.connector.connect(**CONFIG)
    if not connection:
        return None
    
    try:
        cursor=connection.cursor(dictionary=True)

        update_fields={

            "user_name":user_name,
            "surname":surname,
            "is_premium":is_premium,
            "age":age,
            "balance":balance            
        }      
        fields = [f"{key} = %s" for key, value in update_fields.items() if value is not None]
        values=[value for key,value in update_fields.items() if value is not None]

        if not fields:
            print("güncellemek için alan verilmedi")
            return None
        
        query=f"UPDATE user SET {','.join(fields)} WHERE id=%s"
        values.append(user_id)
        cursor.execute(query,values)
        connection.commit()
        print(f"{user_id} kullanicisi güncellendi")
    except Exception as e:
        print("kullanici güncellenemedi")
        print(f"hata:{e}")
        return None
    finally:
        cursor.close()
        connection.close()
update_user(
    user_id=52,
    user_name="Ahmet",
    surname="doğan",
    is_premium=1,
    age=36,
    balance=200
)
print(update_user)



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
print(list_all_users())

#connection.commit() “veritabanındaki değişiklikleri kaydet” anlamına gelir ve sadece INSERT, UPDATE, DELETE gibi işlemlerden sonra kullanılır SELECTte kullanılmaz


        
    


