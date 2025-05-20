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



def create_owner(owner_id, mail,password):
    connection = mysql.connector.connect(**CONFIG)
    if not connection:
        return None
    try:
        cursor = connection.cursor()
        query = """INSERT INTO owner(owner_id, mail,password) VALUES (%s, %s, %s)"""
        values = (owner_id, mail,password)
        cursor.execute(query, values)
        connection.commit()
        print("isletme  oluşturuldu")
    except Exception as e:
        print("isletme oluşturulmadi:", e)
        return None
    finally:
        cursor.close()
        connection.close()
print(create_owner(2,"seher@gmail.com","12345"))


def delete_owner_by_id(owner_id):
    connection = mysql.connector.connect(**CONFIG)
    if not connection:
        return None
    try:
        cursor=connection.cursor(dictionary=True)
        query="DELETE FROM owner WHERE id=%s"
        cursor.execute(query,(owner_id,))
        connection.commit()
        print(f"{owner_id} id'li isletme silindi")
    except Exception as e:
        print("isletme silinmedi")
        print(f"hata:{e}")
        return None
    finally:
        cursor.close()
        connection.close()
print(delete_owner_by_id(2))


def add_owner(mail, password):
    connection = mysql.connector.connect(**CONFIG)
    if not connection:
        return None
    try:
        cursor = connection.cursor(dictionary=True)
        check_query = "SELECT * FROM owner WHERE mail = %s" # mail zaten var mı
        cursor.execute(check_query, (mail,))
        result = cursor.fetchone()
        if result:
            print("bu mail adresiyle zaten kayit olunmuş")
            return "zaten kayitli"

        # 2. Yoksa yeni kayıt ekle
        insert_query = "INSERT INTO owner(mail, password) VALUES(%s, %s)"
        cursor.execute(insert_query, (mail, password))
        connection.commit()
        print("kayit işlemi tamamlandi")
        return "kayit başarili"
    except Exception as e:
        print("kayit başarisiz")
        print(f"Hata: {e}")
        return f"Hata: {e}"
    finally:
        cursor.close()
        connection.close()
#print(add_owner("aaja",12354))


def get_owner_by_id(owner_id): 
    connection=mysql.connector.connect(**CONFIG)
    if not connection: # bağlantı başarısızsa 
        return None # hiçbir şey döndürmez
    try: # hataları yakalamak için deneme bloğu başlar 
        cursor=connection.cursor(dictionary=True) 
        query = "SELECT id FROM food_choice.owner WHERE id=%s" 
        cursor.execute(query,(owner_id,))  # sorguyu çalıştırır %s yerine owner_id  gelir
        owner=cursor.fetchone() # eşleşen bir kullanıcı varsa onu alır
        return f"{owner['id']}" if owner else "kayit bulunmadi"
    except Exception as e: # eğer hata olursa hatayı e nin içine kaydet 
        print("isletme getirilemedi") # hata mesajı yazdırlır 
        print(f"hata:{e}") # hatanın kendisini yazdırılır
        return None 
    finally:
        cursor.close() # cursor kapatılır
        connection.close() # veritabanı bağlantısı kapatılır
#print(get_owner_by_id(5))



def update_owner(owner_id,mail=None,password=None):
    connection=mysql.connector.connect(**CONFIG)
    if not connection:
        return None
    try:
        cursor=connection.cursor(dictionary=True)
        update_fields={
            "mail":mail,
            "password":password,
                   
        }
        fields = [f"{key} = %s" for key, value in update_fields.items() if value is not None]
        values=[value for key,value in update_fields.items() if value is not None]
        if not fields:
            print("güncellemek için alan verilmedi")
            return None  
        query=f"UPDATE owner SET {','.join(fields)} WHERE id=%s"     
        values.append(owner_id)
        cursor.execute(query,values)
        connection.commit()
        print(f"{owner_id}  güncellendi")
    except Exception as e:
        print("isletme güncellenemedi")
        print(f"hata:{e}")
        return None
    finally:
        cursor.close()
        connection.close()
update_owner(
    owner_id=8,
    mail="akyel@gmail.com",
    password=123456

    
)


def list_all_owner():
    connection=mysql.connector.connect(**CONFIG)
    if not connection:
        return None
    try:
        cursor=connection.cursor(dictionary=True)
        query="SELECT*FROM food_choice.owner"
        cursor.execute(query,)
        return cursor.fetchall()
    except Exception as e:
        print("isletme listelenmedi")
        print(f"hata:{e}")
        return None
    finally:
        cursor.close()
        connection.close()



