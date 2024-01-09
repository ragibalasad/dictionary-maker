from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Get the absolute path to the directory where this script is located
basedir = os.path.abspath(os.path.dirname(__file__))

# Use a relative path for the SQLite database file in the same directory as the script
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')
db = SQLAlchemy(app)


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), unique=True, nullable=False)
    transliteration = db.Column(db.String(100), nullable=False)
    meaning = db.Column(db.String(500), nullable=False)
    pos = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)

@app.route('/')
def index():
    entries = Entry.query.all()
    print(entries)
    return render_template('index.html', entries=entries)

@app.route('/entry')
def entry():
    return render_template('entry.html')

def word_exists(word):
    return Entry.query.filter_by(word=word).first() is not None

@app.route('/add_entry', methods=['POST'])
def add_entry():
    word = request.form['word']

    if word_exists(word):
        word_exists_message = f'The word "{word}" already exists.'
        return render_template('entry.html', word_exists_message=word_exists_message)

    transliteration = request.form['transliteration']
    meaning = request.form['meaning']
    pos = request.form['pos']
    category = request.form['category']

    new_entry = Entry(word=word, transliteration=transliteration, meaning=meaning, pos=pos, category=category)
    db.session.add(new_entry)
    db.session.commit()

    success_message = f'The word "{word}" has been added successfully.'
    return render_template('entry.html', success_message=success_message)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
