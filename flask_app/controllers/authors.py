from flask import render_template, redirect, request, url_for
from flask_app import app
from flask_app.models import author, book


@app.route('/authors')
def home_authors():
    return render_template('index.html', authors=author.Author.all_authors())

@app.route('/process/author', methods=['POST'])
def process_author():
    data = {
    'name': request.form['author_name']
    }
    author.Author.save_author(data)
    return redirect('/authors')

@app.route('/author/<int:author_id>')
def show_author(author_id):
    data={
        'id': author_id
    }
    shown_author = author.Author.one_author(data)
    all_books = book.Book.all_books()
    return render_template('show_author.html', author=shown_author, books=all_books)

@app.route('/process/fav_book', methods=['POST'])
def process_author_fav():
    data={
        'book_id':request.form['fav_book'],
        'user_id':request.form['author_id']
    }
    book.Book.fav(data)
    authorid=request.form['author_id']
    return redirect(url_for('.show_author', author_id= authorid))