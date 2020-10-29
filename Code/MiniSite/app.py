import os
import json
from flask import Flask, render_template, request
app = Flask(__name__)


@app.route("/")
def index():
    # read in personas
    with open('ContentSamples/personas.json') as f:
        personas = json.load(f)

    # read in topic summaries from a theme
    with open('ContentSamples/theme.json') as f:
        theme = json.load(f)
        topics = theme[0]['topics']

    return render_template("index.html", personas=personas, topics=topics)


@app.route("/topic")
def topic():
    # read in topic details
    id = request.args.get('id')
    with open('ContentSamples/topic_detail.json') as f:
        topic_detail = json.load(f)
        primary_snippets = topic_detail['primary_snippets']
        secondary_snippets = topic_detail['secondary_snippets']

    return render_template("topic.html", primary_snippets=primary_snippets, secondary_snippets=secondary_snippets)


if __name__ == "__main__":
    port = int(os.getenv('PORT'))
    app.run(debug=True, port=port, host='0.0.0.0')

