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
    try: # hataları yakalamak için deneme bloğu başlar 
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



def get_food_full_info_by_id(food_id):
    connection=mysql.connector.connect(**CONFIG)
    if not connection:
        return None
    try:
        cursor=connection.cursor(dictionary=True)
        query="SELECT * FROM food_choice.food WHERE id=%s"
        cursor.execute(query,(food_id,))
        food=cursor.fetchone()
        return food
    except Exception as e:
        print("yemek getirilemedi")
        print(f"hata:{e}")
        return None
    finally:
        cursor.close()
        connection.close()
print(get_food_full_info_by_id(28))



def add_food(food_name,stock,price,distance):
    connection=mysql.connector.connect(**CONFIG)
    if not connection:
        return None
    try:
        cursor=connection.cursor(dictionary=True)
        query="INSERT INTO food(food_name,stock,price,distance) VALUES(%s,%s,%s,%s)"
        cursor.execute(query,(food_name,stock,price,distance))
        connection.commit()
        print(f"{food_name} yemeği eklendi")
    except Exception as e:
        print("yemegi getirilemedi")
        print(f"hata:{e}")
        return None
    finally:
        cursor.close()
        connection.close()
print(add_food("pilav",5,400,1.5)) 



def delete_food_by_id(food_id):
    connection=mysql.connector.connect(**CONFIG)
    if not connection:
        return None
    try:
        cursor=connection.cursor(dictionary=True)
        query="DELETE FROM food WHERE id=%s"
        cursor.execute(query,(food_id,))
        connection.commit()
        print(f"{food_id} id'li yemek silindi")
    except Exception as e:
        print("yemek silinmedi")
        print(f"hata:{e}")
        return None
    finally:
        cursor.close()
        connection.close()
print(delete_food_by_id(28))


def update_food(food_id,food_name=None,stock=None,price=None,distance=None):
    connection=mysql.connector.connect(**CONFIG)
    if not connection:
        return None
    try:
        cursor=connection.cursor(dictionary=True)

        update_fields={

            "food_name":food_name,
            "stock":stock,
            "price":price,
            "distance":distance,           
        }
        fields = [f"{key} = %s" for key, value in update_fields.items() if value is not None]
        values=[value for key,value in update_fields.items() if value is not None]

        if not fields:
            print("güncellemek için alan verilmedi")
            return None
        
        query=f"UPDATE food SET {','.join(fields)} WHERE id=%s"     
        values.append(food_id)
        cursor.execute(query,values)
        connection.commit()
        print(f"{food_id} kullanicisi güncellendi")
    except Exception as e:
        print("kullanici güncellenemedi")
        print(f"hata:{e}")
        return None
    finally:
        cursor.close()
        connection.close()
update_food(
    food_id=34,
    food_name="kebab",
    stock=13,
    price=250,
    distance=1.5   
)
print(update_food)



def list_all_foods():
    connection=mysql.connector.connect(**CONFIG)
    if not connection:
        return None
    try:
        cursor=connection.cursor(dictionary=True)
        query="SELECT*FROM food_choice.food"
        cursor.execute(query,)
        return cursor.fetchall()
    
    except Exception as e:
        print("yemekler listelenmedi")
        print(f"hata:{e}")
        return None
    finally:
        cursor.close()
        connection.close()
print(list_all_foods())





    

