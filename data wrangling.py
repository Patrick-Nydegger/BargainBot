import spacy
import tqdm
import warnings

# Es kommt immer eine Fehlermeldung bei spacy...
warnings.filterwarnings("ignore", category=UserWarning, message=".*W008.*")

"""
Pipeline die simulierte Daten aus dem Internet validiert, aufbereitet und duch nlp in kategorien ergänzt. 
Danach die SQL INSERT-Statements erzeugt
"""

def database():
    """
    Eine simulierte Datenquelle, wie beispielsweise ein vorbereinigter Output von Webscraping
    """

    new_products = [
        ("Äpfel", 1, "kg"),
        ("Bananen", 1, "kg"),
        ("Kartoffeln", 1, "kg"),
        ("Tomaten", 1, "kg"),
        ("Butter", 25000, "g"),
        ("Eier", 6, "stk"),
        ("Hartkäse", 250, "g"),
        ("Joghurt nature", 200, "g"),
        ("Vollmilch pasteurisiert", 1, "l"),
        ("Haferflocken", 1, "kg"),
        ("Honig", 500, "g"),
        ("Ruchbrot", 500, "G"),
        ("Langkornreis", 1, "KG"),
        ("Spaghetti", 500, "g"),
        ("Weissmehl", 1, "kg"),
        ("Kristallzucker", 1, "kg"),
        ("Mayonnaise Tube", 265, "g"),
        ("Sonnenblumenöl", 1, "l"),
        ("Speisesalz", 1, "kg"),
        ("Bratwurst", 300, "g"),
        ("Forellenfilet geräuchert", 150, "g"),
        ("Pouletgeschnetzeltes", 300, "g"),
        ("Butterguetsli Petit Beurre", 200, "g"),
        ("Lasagne bolognese", 500, "g"),
        ("Milchschokolade", 100, "g"),
        ("Pizza Margherita", 400, "g"),
        ("Pommes-Chips Paprika Beutel", 300, "Gram"),
        ("Kaffeekapseln lungo", 10, "stk"),
        ("Mineralwasser mit Kohlensäure", 1, "l"),
        ("Orangensaft", 1, "l"),
        ("Allzweckreiniger flüssig", 1, "l"),
        ("Geschirrspüler Pulver", 1, "kg"),
        ("Haushaltpapier", 2, "Stück"),
        ("Nastücher", 15, "stückchen"),
        ("Waschmittel (Farbwäsche), flüssig", 1, "liter"),
        ("WC-Papier", 6, "stk"),
        ("Deospray", 150, "ml"),
        ("Duschshampoo", 300, "ml"),
        ("Flüssigseife", 500, "ml"),
        ("Zahnpasta", 125, "ml")]
    return new_products


def mass_to_gramm(value, unit):     # vorausgesetzt g == 9.81 ;)
    """
    Diese Funktion wandelt verschiedene Masseinheiten in Gramm um.
    """

    unit = unit.lower()

    if unit in ['g', 'gram','gramm', 'grams']:
        new_value = value
        new_unit = 'g'

    elif unit in ['mg', 'milligram', 'milligramm','milligrams']:
        new_value = value / 1000
        new_unit = 'g'

    elif unit in ['kg', 'kilogram','kilogramm', 'kilograms']:
        new_value = value * 1000
        new_unit = 'g'

    elif unit in ['t', 'tonne', 'ton', 'tons']:
        new_value = value * 1_000_000
        new_unit = 'g'

    elif unit in ['lb', 'lbs', 'pound', 'pounds', 'pfund']:
        new_value = value * 453.592
        new_unit = 'g'

    elif unit in ['oz', 'ounce', 'ounces','unze']:
        new_value = value * 28.3495
        new_unit = 'g'

    elif unit in ['st', 'stone', 'stones']:  # Stone (Stein)
        new_value = value * 6350.29
        new_unit = 'g'

    else:
        # Falls eine unbekannte Einheit übergeben wird
        new_value = None
        new_unit = None
        print(f"Fehler: Unbekannte Einheit '{unit}'.")

    return new_value, new_unit


def liquid_to_ml(value, unit):
    """
    Diese Funktion wandelt verschiedene Flüssigkeitsmaßeinheiten in Milliliter um.
    """

    unit = unit.lower()

    if unit in ['ml', 'milliliter', 'millilitre']:
        new_value = value
        new_unit = 'ml'

    elif unit in ['cl', 'centiliter', 'centilitre']:
        new_value = value * 10
        new_unit = 'ml'

    elif unit in ['dl', 'deciliter', 'decilitre']:
        new_value = value * 100
        new_unit = 'ml'

    elif unit in ['l', 'liter', 'litre']:
        new_value = value * 1000
        new_unit = 'ml'

    elif unit in ['hl', 'hectoliter', 'hectolitre']:
        new_value = value * 100000
        new_unit = 'ml'

    elif unit in ['gal', 'gallon', 'gallons']:  # Gallone (US Liquid Gallon)
        new_value = value * 3785.41
        new_unit = 'ml'

    elif unit in ['qt', 'quart', 'quarts']:  # Quart (US Liquid Quart)
        new_value = value * 946.353
        new_unit = 'ml'

    elif unit in ['pt', 'pint', 'pints']:  # Pint (US Liquid Pint)
        new_value = value * 473.176
        new_unit = 'ml'

    elif unit in ['cup', 'cups', 'tasse']:  # Tasse (US Legal Cup)
        new_value = value * 240
        new_unit = 'ml'

    elif unit in ['floz', 'fluid ounce', 'fluid ounces']:  # Fluid Ounce (US Fluid Ounce)
        new_value = value * 29.5735
        new_unit = 'ml'

    else:
        # Falls eine unbekannte Einheit übergeben wird
        new_value = None
        new_unit = None
        print(f"Fehler: Unbekannte Einheit '{unit}'.")

    return new_value, new_unit


def validate_products(new_products):
    """
    Diese Funktion organisiert die validation der Produkte.
    """

    validated_products = []
    #print(new_products)
    for tupel in new_products:
        unit = tupel[2]
        if unit.lower() in ['g', 'gram', 'gramm', 'grams',
                        'mg', 'milligram', 'milligramm', 'milligrams',
                        'kg', 'kilogram', 'kilogramm', 'kilograms',
                        't', 'tonne', 'ton', 'tons',
                        'lb', 'lbs', 'pound', 'pounds', 'pfund',
                        'oz', 'ounce', 'ounces', 'unze',
                        'st', 'stone', 'stones']:

            value, unit = mass_to_gramm(tupel[1], tupel[2])
            validated_products.append((tupel[0], value, unit))
            #print(f"Produkt '{tupel[0]}': {value} {unit}")

        elif unit.lower() in ['ml', 'milliliter', 'millilitre',
                            'cl', 'centiliter', 'centilitre',
                            'dl', 'deciliter', 'decilitre',
                            'l', 'liter', 'litre',
                            'hl', 'hectoliter', 'hectolitre',
                            'gal', 'gallon', 'gallons',
                            'qt', 'quart', 'quarts',
                            'pt', 'pint', 'pints',
                            'cup', 'cups',
                            'floz', 'fluid ounce', 'fluid ounces']:

            value, unit = liquid_to_ml(tupel[1], tupel[2])
            validated_products.append((tupel[0], value, unit))
            # print(f"Produkt '{tupel[0]}': {value} {unit}")

        elif unit.lower() in ['stück', 'stückchen', 'stücklein', 'stk', 'st', 'pcs', 'piece', 'pieces']:
            value, unit = tupel[1], 'stk'
            # print(f"Produkt '{tupel[0]}': {value} {unit}")
            validated_products.append((tupel[0], value, unit))

    return validated_products


def spacy_evaluation(productname,nlp):
    """
    Diese Funktion wendet spacy an, um die Produktkategorie zu bestimmen.
    """

    product_data = [
        ("Orangen", 1),
        ("Karotten", 1),
        ("Gurken", 1),
        ("Salat", 1),
        ("Zwiebeln", 1),
        ("Knoblauch", 1),
        ("Zitronen", 1),
        ("Birnen", 1),
        ("Trauben", 1),
        ("Brokkoli", 1),
        ("Äpfel", 1),
        ("Bananen", 1),
        ("Kartoffeln", 1),
        ("Tomaten", 1),
        ("Quark", 2),
        ("Joghurt", 2),
        ("Rahm", 2),
        ("Milch", 2),
        ("Frischkäse", 2),
        ("Mozzarella", 2),
        ("Hüttenkäse", 2),
        ("Feta", 2),
        ("Pudding", 2),
        ("Schlagsahne", 2),
        ("Butter", 2),
        ("Eier", 2),
        ("Hartkäse", 2),
        ("Naturejoghurt", 2),
        ("Vollmilch", 2),
        ("Toastbrot", 3),
        ("Konfitüre", 3),
        ("Erdnussbutter", 3),
        ("Müsli", 3),
        ("Cornflakes", 3),
        ("Zwieback", 3),
        ("Knäckebrot", 3),
        ("Kaffee", 3),
        ("Teebeutel", 3),
        ("Nutella", 3),
        ("Haferflocken", 3),
        ("Honig", 3),
        ("Ruchbrot", 3),
        ("Penne", 4),
        ("Fusilli", 4),
        ("Basmatireis", 4),
        ("Polenta", 4),
        ("Dinkelmehl", 4),
        ("Hartweizengriess", 4),
        ("Couscous", 4),
        ("Nudeln", 4),
        ("Reiswaffeln", 4),
        ("Pizzamehl", 4),
        ("Langkornreis", 4),
        ("Spaghetti", 4),
        ("Weissmehl", 4),
        ("Rohrzucker", 5),
        ("Puderzucker", 5),
        ("Meersalz", 5),
        ("Pfeffer", 5),
        ("Essig", 5),
        ("Olivenöl", 5),
        ("Sonnenblumenöl", 5),
        ("Backpulver", 5),
        ("Vanillezucker", 5),
        ("Ketchup", 5),
        ("Kristallzucker", 5),
        ("Mayonnaise", 5),
        ("Sonnenblumenöl", 5),
        ("Speisesalz", 5),
        ("Rinderhackfleisch", 6),
        ("Pouletbrust", 6),
        ("Lachsfilet", 6),
        ("Thunfisch", 6),
        ("Salami", 6),
        ("Schinken", 6),
        ("Speck", 6),
        ("Crevetten", 6),
        ("Würstchen", 6),
        ("Wienerli", 6),
        ("Fischstäbchen", 6),
        ("Bratwurst", 6),
        ("Forellenfilet", 6),
        ("Pouletgeschnetzeltes", 6),
        ("Tiefkühlpizza", 7),
        ("Suppe", 7),
        ("Gummibärchen", 7),
        ("Kekse", 7),
        ("Schokoriegel", 7),
        ("Nüsse", 7),
        ("Popcorn", 7),
        ("Müsliriegel", 7),
        ("Fertigsalat", 7),
        ("Butterguetsli", 7),
        ("Lasagnebolognese", 7),
        ("Milchschokolade", 7),
        ("Pizza", 7),
        ("Pommeschips", 7),
        ("Apfelsaft", 8),
        ("Cola", 8),
        ("Eistee", 8),
        ("Bier", 8),
        ("Wein", 8),
        ("Espressobohnen", 8),
        ("Tee", 8),
        ("Gemüsesaft", 8),
        ("Energydrink", 8),
        ("Smoothie", 8),
        ("Kaffeekapseln", 8),
        ("Mineralwasser", 8),
        ("Orangensaft", 8),
        ("Spülmittel", 9),
        ("Waschmittel", 9),
        ("Klopapier", 9),
        ("Müllsäcke", 9),
        ("Alufolie", 9),
        ("Frischhaltefolie", 9),
        ("Küchenrolle", 9),
        ("Batterien", 9),
        ("Glühbirnen", 9),
        ("Reinigungstücher", 9),
        ("Allzweckreiniger", 9),
        ("Geschirrspüler", 9),
        ("Haushaltpapier", 9),
        ("Nastücher", 9),
        ("Waschmittel", 9),
        ("Toilettenpapier", 9),
        ("Shampoo", 10),
        ("Duschgel", 10),
        ("Handseife", 10),
        ("Feuchtigkeitscreme", 10),
        ("Zahnbürsten", 10),
        ("Mundspülung", 10),
        ("Rasierschaum", 10),
        ("Bodylotion", 10),
        ("Haarspray", 10),
        ("Tampons", 10),
        ("Deospray", 10),
        ("Duschshampoo", 10),
        ("Flüssigseife", 10),
        ("Zahnpasta", 10)
    ]

    doc = nlp(productname)

    max_similarity = -1
    predicted_category = None

    for product_entry, category_number in product_data:
        similarity = doc.similarity(nlp(product_entry))

        if similarity > max_similarity:
            max_similarity = similarity
            predicted_category = category_number

    # print(f"Produkt '{productname}' wurde der Kategorie {predicted_category} zugeordnet.")
    return predicted_category

def get_categoryname(validated_products,nlp):
    """
    Diese Funktion organisiert die spacy Anwendung
    """


    validated_products_with_category_id = []
    for tupel in tqdm.tqdm(validated_products):
        productname = tupel[0]
        productcategoryproductcategory_id = spacy_evaluation(productname,nlp)
        validated_products_with_category_id.append((tupel[0], tupel[1], tupel[2], productcategoryproductcategory_id))

    #print(f"Validierte Produkte mit Kategorie-ID: {validated_products_with_category_id}")
    return validated_products_with_category_id


def product_insert_statement(validated_products_with_category_id):
    """
    Diese Funktion nimmt eine Liste von Produkten und gibt die SQL Insert Statements zurück.
    """

    insert_statements = []

    for product in validated_products_with_category_id:
        productname, quantity, unit, productcategoryproductcategory_id = product
        statement = (f"INSERT INTO products (productcategoryproductcategory_id, productname, quantity, unit) VALUES "
                     f"('{productcategoryproductcategory_id}','{productname}', {quantity}, '{unit}');")
        insert_statements.append(statement)
        print(statement)


    return insert_statements


def main():
    """
    Diese Funktion organisiert die Pipeline
    """

    new_products = database()
    print("--------Datenvalidierung")
    validated_products = validate_products(new_products)
    print("Kleinschreibung, Einheiten in 'g' , 'ml' und 'stk' umgewandelt und Menge berechnet")
    nlp = spacy.load("de_core_news_md")
    print("--------Produktkategorisierung")
    productcategoryproductcategory_id = get_categoryname(validated_products,nlp)
    print("--------Generierung der Insertstatements")
    product_insert_statement(productcategoryproductcategory_id)
    print("--------Fertig!")
    #Diese INSERT-Statements können dann in eine Datenbank eingefügt werden. (Vorzugsweise über die Verbindung, siehe main.py


main()