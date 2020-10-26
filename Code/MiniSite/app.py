import os
from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/article")
def article():
    return render_template("article.html")


if __name__ == "__main__":
    port = int(os.getenv('PORT'))
    app.run(debug=True, port=port, host='0.0.0.0')

