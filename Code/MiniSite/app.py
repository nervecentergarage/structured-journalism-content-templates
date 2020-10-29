import os
import json
from flask import Flask, render_template, request
app = Flask(__name__)


@app.route("/")
def index():
    personas = [
        {'name': 'persona1', 'id': 'id1'},
        {'name': 'persona2', 'id': 'id2'},
        {'name': 'persona3', 'id': 'id3'}
    ]
    topics = [
        {'id': 'id1', 'heading': 'topic1', 'summary': 'summary1', 'description': 'description1'},
        {'id': 'id2', 'heading': 'topic2', 'summary': 'summary2', 'description': 'description2'},
        {'id': 'id3', 'heading': 'topic3', 'summary': 'summary3', 'description': 'description3'},
        {'id': 'id4', 'heading': 'topic4', 'summary': 'summary4', 'description': 'description4'},
        {'id': 'id5', 'heading': 'topic5', 'summary': 'summary5', 'description': 'description5'},
        {'id': 'id6', 'heading': 'topic6', 'summary': 'summary6', 'description': 'description6'},
        {'id': 'id7', 'heading': 'topic7', 'summary': 'summary7', 'description': 'description7'}
    ]
    return render_template("index.html", personas=personas, topics=topics)


@app.route("/topic")
def topic():
    id = request.args.get('id')
    with open('ContentSamples/topic_detail.json') as f:
        topic_detail = json.load(f)
        primary_snippets = topic_detail['primary_snippets']

    return render_template("topic.html", id=id, primary_snippets=primary_snippets)


if __name__ == "__main__":
    port = int(os.getenv('PORT'))
    app.run(debug=True, port=port, host='0.0.0.0')

