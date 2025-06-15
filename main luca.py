import mysql.connector
from mysql.connector import Error
import datetime
import customtkinter as ctk

# --- Datenbank-Konfiguration ---
HOST = "localhost"
DATABASE = "manuel projekt v4" # Umbenennen auf korrekter Name pn:"biprojekt", ll:"Manuel Projekt V3"
USER = "BargainBot"
PASSWORD = "%BargainBot"
#--------------------------------

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
        #print(f"verbunden.")
        return connection
    except Error:
        return None


def get_productname(product_id):
    """
    Diese Funktion gibt den Produktnamen für eine gegebene Produkt-ID zurück.
    """
    connection = connect_to_database()
    cursor = connection.cursor()

    query = "SELECT productname FROM product WHERE product_id = %s"
    cursor.execute(query, (product_id,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result[0]  # Produktname

def get_all_product_ids():
    """
    Diese Funktion gibt alle Produkt-IDs aus der Datenbank zurück.
    """
    connection = connect_to_database()
    cursor = connection.cursor()

    query = "SELECT product_id FROM product"
    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    all_product_ids = [item[0] for item in results]  # Liste der Produkt-IDs
    return all_product_ids

def get_user_prename(user_id):
    """
    Diese Funktion gibt den Benutzernamen für eine gegebene User-ID zurück.
    """
    connection = connect_to_database()
    cursor = connection.cursor()

    query = "SELECT user.prename FROM user WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result[0]  # Benutzername

def frequency_based_analysis(look_back_weeks=None): #Baseline
    """
    Diese Funktion führt eine Äuffigkeitsanalyse durch, um die am häufigsten
    gekauften Produkte zu ermitteln.
    """

    shoppinglist_id_per_user, user_id = get_shoppinglist_per_user()
    all_products_with_timestamp_per_user= get_all_products_with_timestamp_per_user(shoppinglist_id_per_user)
    #print(get_all_products_with_timestamp_per_user)
    product_quantities = {}
    current_time = datetime.datetime.now() # Aktuelle Zeit für den Bezugspunkt

    user_prename = get_user_prename(user_id)

    for product_id, amount, shoppinglist_id, timestamp in all_products_with_timestamp_per_user:
        # Wenn ein look_back_weeks definiert ist, fwerden die daten gefiltert
        if look_back_weeks is not None:
            time_difference = current_time - timestamp

            if time_difference.days > (look_back_weeks * 7):
                continue # Überspringe Daten, die ausserhalb des Look-Back-Fensters liegen


        if product_id in product_quantities:
            product_quantities[product_id] += amount
        else:
            product_quantities[product_id] = amount


    # Sortiere die Produkte nach ihrer Gesamtmenge in absteigender Reihenfolge
    sorted_products_list = sorted(product_quantities.items(), key=lambda item: item[1], reverse=True) #absteigend

    # Konvertiere die sortierte Liste von Tupeln wieder in ein Dictionary
    sorted_products_dict = dict(sorted_products_list) #{product_id: total_amount, ...}
    # print(sorted_products_dict)

    #Produktnamen aus Datenbank hohlen
    print(60*"#")
    print(f"Top Produkte von {user_prename} in den letzten {look_back_weeks} Wochen:")
    print("Anzahl ¦ Produktname")
    for product_id, amount in sorted_products_dict.items():
        product_name = get_productname(product_id)
        print(f"{amount} ¦ {product_name}")
        #sorted_products_dict[product_name] = sorted_products_dict.pop(id)
    return sorted_products_dict



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

    products_with_timestamp_per_user = []

    for id in shoppinglist_id_per_user:
        cursor.execute(query, (id,))
        results = cursor.fetchall()

        for r in results:
            products_with_timestamp_per_user.append(r)

    #print(products_with_timestamp_per_user)

    cursor.close()
    connection.close()
    return products_with_timestamp_per_user



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
    # print(results)

    cursor.close()
    connection.close()
    shoppinglist_id_per_user = [item[0] for item in results]
    # print(f"shoppinglist_id_per_user: {shoppinglist_id_per_user}")
    return shoppinglist_id_per_user, user_id # example: [1, 2, 3, 4] id der Shoppinlisten vom User

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

def get_cheapest_1_store(shoppinglist_shop_price):
    store_totals = {}

    for amount, product_name, store_name, unit_price in shoppinglist_shop_price:
        total_price = amount * unit_price

        if store_name not in store_totals:
            store_totals[store_name] = 0.0

        store_totals[store_name] += total_price


    for store, total in store_totals.items():
        print(f"{store}: {total:.2f} CHF")
    product_with_assigned_store = [] # [(amount, product_name, store_name, price), ...]

    cheapest_store = min(store_totals, key=store_totals.get)
    print(f"Günstigster Laden: {cheapest_store} mit {store_totals[cheapest_store]:.2f} CHF")

    for amount, product_name, store_name, unit_price in shoppinglist_shop_price:
        if store_name == cheapest_store:
            enhanced_tuple = (amount, product_name, store_name, unit_price)
            product_with_assigned_store.append(enhanced_tuple)

    print(f"Produkt mit zugeordnetem Laden: {product_with_assigned_store}")
    return store_totals, cheapest_store, product_with_assigned_store #[(1, 'Äpfel', 'Aldi', 1.58),..]

def get_cheapest_2_store(shoppinglist_shop_price):
    pass

def get_shopping_list_gui(product_list):
    """
    öffnet ein GUI Fenster mit customTKinter für die Eingabe der Einkaufsliste
    """

    shoppinglist = []

    # Hauptfenster
    app = ctk.CTk()
    app.title("Erstelle hier deine Einkaufsliste")
    app.geometry("400x800")

    # Titel
    title_label = ctk.CTkLabel(master=app, text="Wähle hier die Produkte und gib die Menge an", font=("Verdana", 14))
    title_label.pack(padx=20, pady=(20, 10))

    # Fenster für die Produkte
    scrollable_frame = ctk.CTkScrollableFrame(master=app, label_text="Erhältliche Produkte")
    scrollable_frame.pack(padx=20, pady=10, fill="both", expand=True)

    checkbox_vars = {}
    entry_widgets = {}

    # Produkte
    for product in product_list:

        row_frame = ctk.CTkFrame(master=scrollable_frame)
        row_frame.pack(fill="x", padx=10, pady=5)

        # Checkbox
        checkbox_vars[product] = ctk.StringVar(value="off")
        checkbox = ctk.CTkCheckBox(
            master=row_frame,
            text=product,
            variable=checkbox_vars[product],
            onvalue="on",
            offvalue="off"
        )
        checkbox.pack(side="left", padx=5)

        # Mengenangabe
        entry = ctk.CTkEntry(master=row_frame, width=50, placeholder_text="0")
        entry.pack(side="right", padx=5)
        entry_widgets[product] = entry  # Store the entry widget for later access

    # Eingabeknopf um abzusenden
    def on_confirm_click():
        """
        This function is executed when the button is clicked.
        """
        # Sammeln der Eingaben
        for product, var in checkbox_vars.items():
            if var.get() == "on":
                # Zuordnung der Menge
                quantity_entry = entry_widgets[product]
                quantity_str = quantity_entry.get()
                # Menge zu Zahl konvertieren
                quantity = int(quantity_str) if quantity_str else 1

                if quantity > 0:
                        shoppinglist.append((quantity, product))

        # Fenster schliessen
        app.destroy()

    confirm_button = ctk.CTkButton(master=app, text="Bestätigen und sparen ✅", command=on_confirm_click)
    confirm_button.pack(padx=20, pady=20)

    # Start the GUI and wait
    app.mainloop()

    return shoppinglist

def create_shoppinglist_per_store(product_with_assigned_store):
    """
    Gruppiert Produkte nach dem Laden und gibt ein Dictionary zurück.
    """
    grouped_data = {}

    for amount, product_name, store_name, unit_price in product_with_assigned_store:
        if store_name not in grouped_data:
            grouped_data[store_name] = []

        grouped_data[store_name].append((amount, product_name, unit_price))

    for store, products in grouped_data.items():
        print(f"\n------ {store} ------")
        for product_info in products:
            amount, product_name, unit_price = product_info
            print(f"  {amount}x {product_name} zu {unit_price:.2f} CHF")

    return grouped_data
def main():
    """
    Main function to run the script.
    """

    print("Willkommen beim BargainBot!")

    number_of_stores = int(input("Anzahl der Läden in denen du einkaufen möchtest: "))
    all_product_ids = get_all_product_ids()
    available_products = [get_productname(product_id) for product_id in all_product_ids]



    shoppinglist = get_shopping_list_gui(available_products)

    print(f"shoppinglist = {shoppinglist}")

    shoppinglist_shop_price = get_price(shoppinglist)
    if number_of_stores == 1:
        store_totals, cheapest_store,product_with_assigned_store = get_cheapest_1_store(shoppinglist_shop_price) #Einfache summenberechung
    elif number_of_stores > 1:
        store_totals, cheapest_store, product_with_assigned_store = get_cheapest_2_store(shoppinglist_shop_price) #Paarweise Berechnung pro Produkt, dann auswahl der insgesammt besten paare

    shoppinglist_per_store = create_shoppinglist_per_store(product_with_assigned_store)



if __name__ == "__main__":
    #shoppinglist_id = int(input("Shopping-List ID: "))

    #shoppinglist = get_shoppinglist(shoppinglist_id)
    #shoppinglist_shop_price = get_price(shoppinglist)
    #get_cheapest_store(shoppinglist_shop_price)
    #shoppinglist_id_per_user = get_shoppinglist_per_user()
    #products_with_timestamp_per_user = get_all_products_with_timestamp_per_user(shoppinglist_id_per_user)
    weeks=[1, 2, 3, 4, 10, 20, 30, 40, 50] # Look-Back-Wochen
    #for week in weeks:
    #    sorted_products_dict = frequency_based_analysis(week)
    main()