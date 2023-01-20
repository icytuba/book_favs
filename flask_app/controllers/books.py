from flask import render_template, redirect, request, url_for
from flask_app import app
from flask_app.models import book, author

@app.route('/books')
def home_books():
    return render_template('home_books.html', books = book.Book.all_books())

@app.route('/process/book', methods=["POST"])
def process_book():
    data={
        'title':request.form['book_title'],
        'np':request.form['num_pages']
    }
    book.Book.save_book(data)
    return redirect('/books')

@app.route('/book/<int:book_id>')
def show_book(book_id):
    data={
        'id':book_id
    }
    shown_book = book.Book.one_book(data)
    # todos_authors=author.Author.all_authors()
    # shown_book_authors=[]
    # for autho in todos_authors:
    #     if isinstance(autho, shown_book.authors):
    #         continue
    #     shown_book_authors.append(author)
    all_authors = author.Author.all_authors()
    return render_template('show_book.html', book=shown_book, authors=all_authors)

@app.route('/process/fav_author', methods=['POST'])
def process_book_fav():
    data={
        'book_id':request.form['book_id'],
        'user_id':request.form['fav_author']
    }
    book.Book.fav(data)
    bookid=request.form['book_id']
    return redirect(url_for('.show_book', book_id= bookid))