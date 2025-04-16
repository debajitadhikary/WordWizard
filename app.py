from flask import Flask, render_template, request
import sqlite3
import math

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('search.html')

@app.route('/search')
def search():
    query = request.args.get('query', '').strip()
    page = int(request.args.get('page', 1))
    per_page = 10  # You can change this value if you want more/less results per page

    if query:
        conn = sqlite3.connect('_dictionary.db')
        cur = conn.cursor()

        # Count total matching results
        cur.execute("SELECT COUNT(*) FROM words WHERE word LIKE ?", ('%' + query + '%',))
        total_results = cur.fetchone()[0]

        total_pages = math.ceil(total_results / per_page)
        offset = (page - 1) * per_page

        # Fetch paginated results
        cur.execute(
            "SELECT * FROM words WHERE word LIKE ? LIMIT ? OFFSET ?",
            ('%' + query + '%', per_page, offset)
        )
        results = cur.fetchall()
        conn.close()

        if results:
            return render_template(
                'search.html',
                results=results,
                query=query,
                page=page,
                total_pages=total_pages
            )
        else:
            return render_template(
                'search.html',
                query=query,
                page=page,
                total_pages=total_pages,
                no_results=True
            )

    return render_template('search.html')
