from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# -----------------------------------------
# MySQL CONNECTION FUNCTION
# -----------------------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",        # <-- apna MySQL user
        password="",        # <-- agar password hai to yahan likho
        database="book_db"   # <-- database name
    )

# -----------------------------------------
# LIST ALL BOOKS + SEARCH
# -----------------------------------------
@app.route("/")
def list_books():
    keyword = request.args.get("search", "")

    conn = get_connection()
    cursor = conn.cursor()

    if keyword:
        cursor.execute("""
            SELECT * FROM books
            WHERE title LIKE %s OR author LIKE %s
        """, (f"%{keyword}%", f"%{keyword}%"))
    else:
        cursor.execute("SELECT * FROM books")

    books = cursor.fetchall()
    conn.close()

    return render_template("books.html", books=books, keyword=keyword)

# -----------------------------------------
# ADD BOOK
# -----------------------------------------
@app.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        price = request.form["price"]
        year = request.form["year"]

        if not title or not author:
            return "Title & Author are required!"

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO books (title, author, price, published_year, created_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (title, author, price or None, year or None, created_at))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add_book.html")

# -----------------------------------------
# EDIT BOOK
# -----------------------------------------
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_book(id):
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        price = request.form["price"]
        year = request.form["year"]

        cursor.execute("""
            UPDATE books
            SET title=%s, author=%s, price=%s, published_year=%s
            WHERE id=%s
        """, (title, author, price or None, year or None, id))

        conn.commit()
        conn.close()
        return redirect("/")

    cursor.execute("SELECT * FROM books WHERE id=%s", (id,))
    book = cursor.fetchone()
    conn.close()

    return render_template("edit_book.html", book=book)

# -----------------------------------------
# DELETE BOOK
# -----------------------------------------
@app.route("/delete/<int:id>")
def delete_book(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM books WHERE id=%s", (id,))
    conn.commit()

    conn.close()

    return redirect("/")

# -----------------------------------------
# RUN THE APP
# -----------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
