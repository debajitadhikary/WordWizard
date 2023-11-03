from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('search.html')

@app.route('/search')
def search():
    query = request.args.get('query')
    if query:
        conn = sqlite3.connect('_dictionary.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM words WHERE word=?", (query,))
        results = cur.fetchall()
        conn.close()
        if results:
            return render_template('search.html', results=results)
        else:
            return render_template('search.html', no_results=True)
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
    # app.run(debug=True)

