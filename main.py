import mysql.connector
from mysql.connector import Error

# --- Datenbank-Konfiguration ---
HOST = "localhost"
DATABASE = "biprojekt" # Umbenennen auf korrekter Name
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

def optimize_shopping_list():
    pass

def calculate_price_with_amounts(found_products, shopping_list_dict):
    found_products_with_amounts = []
    for i in found_products:
        product_name = i[0]
        store_name = i[1]
        price = i[2]

        quantity = shopping_list_dict[product_name]
        total_price = price * quantity
        #print(f"{quantity}x {product_name} von {store_name} kostet insgesamt: {total_price:.2f} Fr.")

        found_products_with_amount_tupel = (product_name, store_name, total_price)
        found_products_with_amounts.append(found_products_with_amount_tupel)


    print(f"Produktpreise mit Menge verrechnet: {found_products_with_amounts}")
    return found_products_with_amounts



def main():
    """
    Das ist die Hauptfunktion, die das Programm steuert.
    """
    print("########## Willkommen beim BargainBot ##########")

    # Eingabe der Produkte
    # Die Eingabe "Apfel, Banane, Milch" wird in eine Liste umgewandelt: ['5:Äpfel', ' Banane', ' Milch']
    items_input = input("Gib die Produkte ein, die du suchst (durch Komma getrennt): ")

    # Dictionary zum Speichern der Produkte und ihrer Mengen
    shopping_list_dict = {}

    for item_str in items_input.split(','):
        item_str = item_str.strip()  # Leerzeichen am Anfang/Ende entfernen

        if ':' in item_str:
            # Wenn ein Doppelpunkt vorhanden ist, teilen wir den String dort
            parts = item_str.split(':', 1)  # Teile maximal einmal am Doppelpunkt

            # Menge verarbeiten
            quantity_str = parts[0].strip()
            product_name = parts[1].strip()

            quantity = int(quantity_str)
            shopping_list_dict[product_name] = quantity
        else:
            quantity = 1  # Standardmenge ist 1, wenn kein Doppelpunkt vorhanden ist
            product_name = item_str.strip()
            shopping_list_dict[product_name] = quantity



    product_list = list(shopping_list_dict.keys())


    # Eine leere Liste, in der wir die gefundenen Produkte speichern
    found_products = []

    # Verbindung zur Datenbank herstellen
    connection = connect_to_database()


    try:
        # Einen Cursor erstellen, um SQL-Befehle auszuführen
        cursor = connection.cursor()

        # Wir gehen die Liste der gewünschten Produkte einzeln durch.
        for product_name in product_list:
            clean_product_name = product_name.strip() # .strip() entfernt Leerzeichen am Anfang und Ende

            print(f"--- Suche nach '{clean_product_name}' in der Datenbank... ---")

            # Suche nach Produktpreis in allen Läden
            query = f"SELECT product.productname, store.name, store_product.price FROM product JOIN store_product ON product.product_id = store_product.productproduct_id  JOIN store ON store_product.storestore_id = store.store_id WHERE  product.productname = %s;"

            cursor.execute(query, (clean_product_name,))

            # Holt alle Ergebnisse, die zur Abfrage passen
            records = cursor.fetchall()

            if not records:
                # Wenn die Liste 'records' leer ist, wurde nichts gefunden.
                print(f"Keine Einträge für '{clean_product_name}' gefunden.")
            else:
                # Wenn wir etwas gefunden haben, gehen wir die Ergebnisse durch
                for row in records:
                    # 'row' ist ein Tupel, z.B. ('Apfel', Migros, '1.58')
                    # Wir fügen die gefundenen Daten zu unserer Liste hinzu
                    found_products.append(row)
                    #print(f"Gefunden: Produkt: {row[0]}, Laden: {row[1]}, Preis: {row[2]} Fr.")

    except Error as e:
        print(f"Ein Fehler ist bei der Datenbankabfrage aufgetreten: {e}")

    finally:
        # 4. Verbindung zur Datenbank schließen
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("\nDie Datenbankverbindung wurde geschlossen.")
            print(f" Auszug aus Datenbank: {found_products}")
            print(f"Datenstruktur bei eingabe mit Menge: {shopping_list_dict}")
            calculate_price_with_amounts(found_products, shopping_list_dict)





if __name__ == "__main__":
    main()