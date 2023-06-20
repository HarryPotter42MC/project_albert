import sqlite3
from flask import Flask, session, render_template, request, g

app = Flask(__name__)
app.secret_key = "password"

def get_db_connection():
    conn = sqlite3.connect('articles.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    articlesRaw = conn.execute('SELECT name, price, quantity, unit, ingredients, nutritional_values FROM articles').fetchall()
    conn.close()
    articles = []
    for articleRaw in articlesRaw:
        article = dict(zip(articleRaw.keys(), articleRaw))
        nuts = dict()
        for nutritional_pair in articleRaw['nutritional_values'].split("\n"):
            nutrient, value = nutritional_pair.split(": ")
            nuts[nutrient] = value
        article['nuts'] = nuts
        articles.append(article)
    return render_template('index.html', article=articles)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('articles.db')
        cursor = db.cursor()
        cursor.execute("select * from articles")
        row_factory = sqlite3.Row
    return cursor.fetchall()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run()