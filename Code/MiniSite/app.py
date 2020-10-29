import os
from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def index():
    personas = [
        {'name': 'persona1', 'id': 'id1'},
        {'name': 'persona2', 'id': 'id2'},
        {'name': 'persona3', 'id': 'id3'}
    ]
    return render_template("index.html", personas=personas)


@app.route("/article")
def article():
    return render_template("article.html")


if __name__ == "__main__":
    port = int(os.getenv('PORT'))
    app.run(debug=True, port=port, host='0.0.0.0')

