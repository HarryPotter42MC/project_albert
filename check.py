import sqlite3

conn = sqlite3.connect("dexify.db")
cursor = conn.cursor()


for row in cursor.execute("select name, price, quantity, unit, ingredients, nutritional_values from articles"):
    name, price, quantity, unit, ingredients, nutritional_values = row

    print(name)
    nuts = dict()
    for nutritional_pair in nutritional_values.split("\n"):
        nutrient, value = nutritional_pair.split(": ")
        nuts[nutrient] = value

    for nutrient, value in nuts.items():
        print(nutrient, value)

conn.close