from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Load existing data from the Excel file if it exists
try:
    df = pd.read_excel('entries.xlsx')
    data = df.to_dict('records')
except FileNotFoundError:
    data = []

@app.route('/')
def index():
    word_count = len(data)
    return render_template('index.html', entries=data, word_count=word_count)


@app.route('/entry')
def entry():
    return render_template('entry.html')

def word_exists(word):
    # Check if the word already exists in the data
    return any(entry['Word'].lower() == word.lower() for entry in data)

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

    entry = {'Word': word, 'Transliteration': transliteration, 'Meaning': meaning, 'POS': pos, 'Category': category}
    data.append(entry)

    # Convert data to DataFrame and save to Excel file
    df = pd.DataFrame(data)
    df.to_excel('entries.xlsx', index=False)

    success_message = f'The word "{word}" has been added successfully.'
    return render_template('entry.html', success_message=success_message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
