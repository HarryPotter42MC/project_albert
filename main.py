import sqlite3


conn = sqlite3.connect("articles.db")


cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        price FLOAT NOT NULL,
        quantity INTEGER NOT NULL,
        unit TEXT NOT NULL,
        ingredients TEXT,
        nutritional_values TEXT
    )
""")

cursor.execute("SELECT COUNT(*) FROM articles")
num_articles = cursor.fetchone()[0]
print(f"There are currently {num_articles} articles in the database.")


list_articles = input("Do you want to list the names of articles in the database? (y/n) ").lower() == "y"
if list_articles:
    cursor.execute("SELECT name FROM articles")
    article_names = cursor.fetchall()
    print("Names of articles in the database:")
    for name in article_names:
        print(name[0])

while True:
    # Ask for the name of the article
    article_name = input("\nArticle name: ")

    # Ask for the ingredients of the article
    ingredients = []
    while True:
        ingredient = input("Ingredient name: ")
        if not ingredient:
            break
        ingredients.append(ingredient)

    # Ask for the nutritional values of the article
    nutritional_values = []
    while True:
        nutritional_value_name = input("Nutritional value name: ")
        if not nutritional_value_name:
            break
        while True:
            nutritional_value_quantity = input("Nutritional value quantity: ")
            try:
                nutritional_value_quantity = float(nutritional_value_quantity)
                break
            except ValueError:
                print("Invalid input. Please enter a numerical value.")
        nutritional_values.append((nutritional_value_name, nutritional_value_quantity))

    # Ask for the price, quantity, and unit of the article
    while True:
        try:
            price = float(input("Price (in euros): "))
            quantity = int(input("Quantity: "))
            try:
                unit = input("Unit of measure (g or l): ")
                if unit not in ["g", "l"]:
                    raise ValueError("Invalid unit of measure. Please enter 'g' or 'l'.")
            except:
                print("unit error")
            break
        except ValueError:
            print("Invalid input. Please enter a numerical value.")

    # Add the article to the database
    try:
        cursor.execute("""
            INSERT INTO articles (name, price, quantity, unit, ingredients, nutritional_values)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (article_name, price, quantity, unit, "\n".join(ingredients), "\n".join([f"{name}: {quantity}" for name, quantity in nutritional_values])))
        conn.commit()
        print("Article added to the database.")
    except sqlite3.IntegrityError:
        print("An article with that name already exists in the database. Please choose a different name.")
    
    # Ask if the user wants to add another article
    add_another_article = input("Enter more articles? (y/n) ").lower() == "y"
    if not add_another_article:
        break

# Close the database connection
conn.commit()
conn.close()
