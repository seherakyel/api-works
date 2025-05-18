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
        query = """INSERT INTO company (owner_id, company_name, description) VALUES (%s, %s, %s)"""
        values = (owner_id, company_name, description)
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
        query="DELETE FROM food WHERE id=%s"
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