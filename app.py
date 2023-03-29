from flask import Flask, make_response,jsonify, request
import sqlite3

conn = sqlite3.connect("books.db")
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name text,
        author text
    )""")

conn.commit()
conn.close()

app = Flask(__name__)

@app.route('/api/books', methods=["GET", "POST"])
def api_books():
    if request.method == "GET":
        conn = sqlite3.connect("books.db")
        c = conn.cursor()
        c.execute("SELECT * FROM books")    
        books = c.fetchall()  

        conn.commit()
        conn.close()
        return make_response(jsonify(books), 200)
    elif request.method == "POST":
        conn = sqlite3.connect("books.db")
        c = conn.cursor()

        query = "INSERT INTO books (name, author) VALUES (?, ?)"

        data = request.json
        name = data["name"]
        author = data["author"]

        c.execute(query, (name, author))    

        last_row_id = c.lastrowid
        c.execute("SELECT * FROM books WHERE id=?", (last_row_id,))
        last_record = c.fetchone()

        conn.commit()
        conn.close()
        return make_response(jsonify(last_record), 201)
    
    

@app.route('/api/books/<book_id>', methods=["GET", "DELETE"])
def get_book(book_id):
    if request.method == "GET":
        conn = sqlite3.connect("books.db")
        c = conn.cursor()  

        c.execute("SELECT * FROM books WHERE id=?", (book_id))
        book = c.fetchone()

        conn.commit()
        conn.close()
        return make_response(jsonify(book), 200)
    elif request.method == "DELETE":
        conn = sqlite3.connect("books.db")
        c = conn.cursor()  

        c.execute("DELETE FROM books WHERE id=?", (book_id))

        conn.commit()
        conn.close()
        return "Success"

@app.route('/api/books', methods=["PUT"])
def update_book():
    conn = sqlite3.connect("books.db")
    c = conn.cursor()  

    data = request.json
    book_id = data["id"]
    name = data["name"]
    author = data["author"]

    c.execute("UPDATE books SET name=?, author=? WHERE id=?", (name, author, book_id))

    conn.commit()
    conn.close()
    return "Success"
    


if __name__ == '__main__':
    app.run(debug=True)