import os
import json
from http.cookies import SimpleCookie

from flask import Flask, render_template, request
app = Flask(__name__)

# used to store persona preference selections from the user
persona_values = {}

# used to store the calculated affinities that the current user has for each snippet type
snippet_affinities = []

# read in definitions of the persona definitions
with open('ContentSamples/personas.json') as f:
    persona_definitions = json.load(f)


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


@app.route("/update-persona")
def updatePersona():
    # store the persona values selected in the user experience
    persona_selections = request.args.get('selections')

    cookie = SimpleCookie()
    cookie.load(persona_selections)

    for key, entry in cookie.items():
        persona_values[key] = entry.value

    print("persona updated: " + str(persona_values))

    update_snippet_affinities()

    return ""


def snippet_affinity(snippet_type):
    persona_multiplier = 0
    # calculate a linear combination of persona affinities for the snippet type
    for persona_type in persona_definitions:
        try:
            persona_multiplier += persona_type['affinities'][snippet_type] * float(persona_values[persona_type['personaID']])
        except:
            # ignore if there is no recorded persona score
            pass
    return persona_multiplier


def update_snippet_affinities():
    # every persona definition should include all affinities. step through the
    # affinities listed in the very first persona definition
    snippet_affinities = []
    for snippet_type in persona_definitions[0]['affinities']:
        affinity_entry = {
            "snippet_type": snippet_type,
            "snippet_affinity": snippet_affinity(snippet_type)
        }
        snippet_affinities.append(affinity_entry)
    print('snippet affinities: ' + str(snippet_affinities))


if __name__ == "__main__":
    port = int(os.getenv('PORT'))
    app.run(debug=True, port=port, host='0.0.0.0')

