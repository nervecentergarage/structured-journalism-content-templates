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
    topics = [
        {'heading': 'topic1', 'summary': 'summary1', 'description': 'description1'},
        {'heading': 'topic2', 'summary': 'summary2', 'description': 'description2'},
        {'heading': 'topic3', 'summary': 'summary3', 'description': 'description3'},
        {'heading': 'topic4', 'summary': 'summary4', 'description': 'description4'},
        {'heading': 'topic5', 'summary': 'summary5', 'description': 'description5'},
        {'heading': 'topic6', 'summary': 'summary6', 'description': 'description6'},
        {'heading': 'topic7', 'summary': 'summary7', 'description': 'description7'}
    ]
    return render_template("index.html", personas=personas, topics=topics)


@app.route("/article")
def article():
    return render_template("article.html")


if __name__ == "__main__":
    port = int(os.getenv('PORT'))
    app.run(debug=True, port=port, host='0.0.0.0')

