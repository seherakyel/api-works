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



def get_order_by_id(order_id):
    connection = mysql.connector.connect(**CONFIG)
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM orders")
        results = cursor.fetchall()
        for order in results:
            print(order)
        return results
    finally:
        cursor.close()
        connection.close()
print(get_order_by_id(2))



def add_order(user_id, food_id, status, payment):
    connection = mysql.connector.connect(**CONFIG)
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO orders (user_id, food_id, order_status, order_payment, order_time)
            VALUES (%s, %s, %s, %s, NOW())
        """
        cursor.execute(query, (user_id, food_id, status, payment))
        connection.commit()
        print("Sipariş başarıyla eklendi.")
    finally:
        cursor.close()
        connection.close()
print(add_order(1,2,"completed","online"))



def delete_order_by_id(order_id):
    connection = mysql.connector.connect(**CONFIG)
    try:
        cursor = connection.cursor()
        query = "DELETE FROM orders WHERE id = %s"
        cursor.execute(query, (order_id,))
        connection.commit()
        print(f"{order_id} numaralı sipariş silindi.")
    finally:
        cursor.close()
        connection.close()
print(get_order_by_id(1))



def update_order(order_id, new_status, new_payment):
    connection = mysql.connector.connect(**CONFIG)
    try:
        cursor = connection.cursor()
        query = """
            UPDATE orders
            SET order_status = %s, order_payment = %s
            WHERE id = %s
        """
        cursor.execute(query, (new_status, new_payment, order_id))
        connection.commit()
        print(f"{order_id} numaralı sipariş güncellendi.")
    finally:
        cursor.close()
        connection.close()
print(2,"pending","cash")


def list_all_orders():
    connection=mysql.connector.connect(**CONFIG)
    if not connection:
        return None
    try:
        cursor=connection.cursor(dictionary=True)
        query="SELECT * FROM food_choice.orders"
        cursor.execute(query,)
        return cursor.fetchall()
    except Exception as e:
        print("sipariş listelenemedi")
        print(f"hata:{e}")
        return None
    finally:
        cursor.close()
        connection.close()
print(list_all_orders())



def get_orders_by_id(user_id):
    connection=mysql.connector.connect(**CONFIG)
    if not connection:
        return None
    try:
        cursor=connection.cursor(dictionary=True)
        query = "SELECT * FROM food_choice.orders WHERE user_id = %s"
        cursor.execute(query,(user_id,))
        orders = cursor.fetchall() 
        return orders
    except Exception as e:
        print("kullanıcya göre siparis getirilmedi")
        print(f"hata:{e}")
        return None
    finally:
        cursor.close()
        connection.close()
print(get_orders_by_id(4))
