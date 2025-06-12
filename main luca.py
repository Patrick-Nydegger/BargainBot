import mysql.connector
from mysql.connector import Error

# --- Datenbank-Konfiguration ---
HOST = "localhost"
DATABASE = "biprojekt" # Umbenennen auf korrekter Name pn:"biprojekt", ll:"Manuel Projekt V3"
USER = "BargainBot"
PASSWORD = "%BargainBot"


def connect_to_database():
    """
    Stellt eine Verbindung zur Datenbank her und gibt das
    Verbindungs-Objekt zurück
    """

    try:
        connection = mysql.connector.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD
        )
        print(f"verbunden.")
        return connection
    except Error:
        return None

def get_all_products_with_timestamp_per_user(shoppinglist_id_per_user):
    """
    Die Funktion exttrahiert füre eine shoppinglist_id alle Produkte mit der Menge und dem Zeitstempel
    """
    connection = connect_to_database()
    cursor = connection.cursor()

    query = """ 
            SELECT product_shoppinglist.productproduct_id, product_shoppinglist.amount, 
            product_shoppinglist.Shoppinglistshoppinglist_id, shoppinglist.timestamp FROM product_shoppinglist JOIN 
            product ON product_shoppinglist.productproduct_id = product.product_id JOIN 
            shoppinglist ON shoppinglist.shoppinglist_id = product_shoppinglist.shoppinglistshoppinglist_id  
            WHERE product_shoppinglist.shoppinglistshoppinglist_id = %s;
        """

    for id in shoppinglist_id_per_user:
        cursor.execute(query, (id,))
        results = cursor.fetchall()
        print(results)

        products_with_timestamp_per_use = 111111111 #noch entpacken und in eine sinvolle Datenstruktur bringen
    cursor.close()
    connection.close()
    return products_with_timestamp_per_use



def get_shoppinglist_per_user(user_id=None):
    """ Die Funktion gibt alle shoppinglist_id's eines Users zurück, der user wird """
    if user_id is None:
        user_id = int(input("User ID: "))

    connection = connect_to_database()
    cursor = connection.cursor()
    query = """
            SELECT shoppinglist.shoppinglist_id, shoppinglist.timestamp
            FROM shoppinglist
            WHERE useruser_id = %s;
            """
    cursor.execute(query, (user_id,))
    results = cursor.fetchall()
    print(results)

    cursor.close()
    connection.close()
    shoppinglist_id_per_user = [item[0] for item in results]
    print(f"shoppinglist_id_per_user: {shoppinglist_id_per_user}")
    return shoppinglist_id_per_user # example: [1, 2, 3, 4] id der Shoppinlisten vom User

def get_shoppinglist(shoppinglist_id):
    connection = connect_to_database()
    cursor = connection.cursor()

    query = """
            SELECT product.productname, product_shoppinglist.amount
            FROM product_shoppinglist JOIN product ON product_shoppinglist.Productproduct_id = product.product_id 
            WHERE product_shoppinglist.Shoppinglistshoppinglist_id = %s;
            """

    cursor.execute(query, (shoppinglist_id,))
    results = cursor.fetchall()

    shoppinglist = [(amount, product_name) for product_name, amount in results]
    print(f"shoppinglist{shoppinglist}")

    cursor.close()
    connection.close()
    return shoppinglist

def get_price(shoppinglist):
    connection = connect_to_database()
    cursor = connection.cursor()

    shoppinglist_shop_price = []

    for amount, product_name in shoppinglist:
        query = """
        SELECT s.name, sp.price
        FROM product p
        JOIN store_product sp ON p.product_id = sp.productproduct_id
        JOIN store s ON sp.storestore_id = s.store_id
        WHERE p.productname = %s;
        """
        cursor.execute(query, (product_name,))
        results = cursor.fetchall()

        for store_name, price in results: shoppinglist_shop_price.append((amount, product_name, store_name, price))

    print(f"shoppinglist_shop_price{shoppinglist_shop_price}")

    cursor.close()
    connection.close()
    return shoppinglist_shop_price

def get_cheapest_store(shoppinglist_shop_price):
    store_totals = {}

    for amount, product_name, store_name, unit_price in shoppinglist_shop_price:
        total_price = amount * unit_price

        if store_name not in store_totals:
            store_totals[store_name] = 0.0

        store_totals[store_name] += total_price


    for store, total in store_totals.items():
        print(f"{store}: {total:.2f} CHF")


    cheapest_store = min(store_totals, key=store_totals.get)
    print(f"Günstigster Laden: {cheapest_store} mit {store_totals[cheapest_store]:.2f} CHF")

    return store_totals, cheapest_store


if __name__ == "__main__":
    shoppinglist_id = int(input("Shopping-List ID: "))

    shoppinglist = get_shoppinglist(shoppinglist_id)
    shoppinglist_shop_price = get_price(shoppinglist)
    get_cheapest_store(shoppinglist_shop_price)
    shoppinglist_id_per_user = get_shoppinglist_per_user()
    products_with_timestamp_per_user = get_all_products_with_timestamp_per_user(shoppinglist_id_per_user)
