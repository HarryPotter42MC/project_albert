from flask import Flask, render_template
import sqlite3

app = Flask("read")

@app.route("/articles")
def articles():
    conn = sqlite3.connect("articles.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM articles")
    num_articles = cursor.fetchone()[0]
    return(f"There are currently {num_articles} articles in the database.")

@app.route("/list")
def list():
    conn = sqlite3.connect("articles.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM articles")
    article_names = cursor.fetchall()
    for name in article_names:
        return(name[0])
    


@app.route("/application")
def ap():
    conn = sqlite3.connect("articles.db")
    cursor = conn.cursor()