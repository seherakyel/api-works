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
    connection = None
    cursor = None  
    try:
        connection = mysql.connector.connect(**CONFIG)
        cursor = connection.cursor()
        query = """INSERT INTO company (owner_id, company_name, description) VALUES (%s, %s, %s)"""
        values = (owner_id, company_name, description)
        cursor.execute(query, values)
        connection.commit()
        print("sirket  oluşturuldu")
    except Exception as e:
        print("Hata oluştu:", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
print(create_company(6,"b","A"))