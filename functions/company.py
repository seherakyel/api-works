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



def create_company(owner_id, company_name, description):
    connection = mysql.connector.connect(**CONFIG)
    if not connection:
        return None
    try:
        cursor = connection.cursor()
        query = """INSERT INTO company(owner_id, company_name, description) VALUES (%s, %s, %s)"""
        values = (owner_id,company_name,description)
        cursor.execute(query, values)
        connection.commit()
        print("sirket  oluşturuldu")
    except Exception as e:
        print("Hata oluştu:", e)
        return None
    finally:
        cursor.close()
        connection.close()
#print(create_company(1,"b","A"))



def delete_company_by_id(company_id):
    connection = mysql.connector.connect(**CONFIG)
    if not connection:
        return None
    try:
        cursor=connection.cursor(dictionary=True)
        query="DELETE FROM company WHERE id=%s"
        cursor.execute(query,(company_id,))
        connection.commit()
        print(f"{company_id} id'li sirket silindi")
    except Exception as e:
        print("sirket silinmedi")
        print(f"hata:{e}")
        return None
    finally:
        cursor.close()
        connection.close()
#print(delete_company_by_id(2))


def add_company( company_name, description):
    connection=mysql.connector.connect(**CONFIG)
    if not connection:
        return None
    try:
        cursor=connection.cursor(dictionary=True)
        query="INSERT INTO company(company_name, description) VALUES(%s,%s)"
        cursor.execute(query,( company_name, description,))
        connection.commit()
        print(f"{company_name} sirketi eklendi")
    except Exception as e:
        print("sirket eklenmedi")
        print(f"hata:{e}")
        return None
    finally:
        cursor.close()
        connection.close()
#print(add_company("aaja","ckJSO"))


def get_company_by_id(company_id): 
    connection=mysql.connector.connect(**CONFIG)
    if not connection: # bağlantı başarısızsa 
        return None # hiçbir şey döndürmez
    try: # hataları yakalamak için deneme bloğu başlar 
        cursor=connection.cursor(dictionary=True) 
        query = "SELECT company_name FROM food_choice.company WHERE id=%s" 
        cursor.execute(query,(company_id,))  # sorguyu çalıştırır %s yerine company_id  gelir
        user=cursor.fetchone() # eşleşen bir kullanıcı varsa onu alır
        return f"{user['company_name']}" #
    except Exception as e: # eğer hata olursa hatayı e nin içine kaydet 
        print("sirket getirilemedi") # hata mesajı yazdırlır 
        print(f"hata:{e}") # hatanın kendisini yazdırılır
        return None 
    finally:
        cursor.close() # cursor kapatılır
        connection.close() # veritabanı bağlantısı kapatılır
#print(get_company_by_id(17))



def update_company(company_id,company_name=None,description=None):
    connection=mysql.connector.connect(**CONFIG)
    if not connection:
        return None
    try:
        cursor=connection.cursor(dictionary=True)
        update_fields={
            "company_name":company_name,
            "description":description,
                   
        }
        fields = [f"{key} = %s" for key, value in update_fields.items() if value is not None]
        values=[value for key,value in update_fields.items() if value is not None]
        if not fields:
            print("güncellemek için alan verilmedi")
            return None  
        query=f"UPDATE company SET {','.join(fields)} WHERE id=%s"     
        values.append(company_id)
        cursor.execute(query,values)
        connection.commit()
        print(f"{company_id} isletme güncellendi")
    except Exception as e:
        print("isletme güncellenemedi")
        print(f"hata:{e}")
        return None
    finally:
        cursor.close()
        connection.close()
update_company(
    company_id=25,
    company_name="sjdhıa",
    description="JBXANDK"
)
#print(update_company)



def list_all_company():
    connection=mysql.connector.connect(**CONFIG)
    if not connection:
        return None
    try:
        cursor=connection.cursor(dictionary=True)
        query="SELECT*FROM food_choice.company"
        cursor.execute(query,)
        return cursor.fetchall()
    
    except Exception as e:
        print("isletme listelenmedi")
        print(f"hata:{e}")
        return None
    finally:
        cursor.close()
        connection.close()
#print(list_all_company())






