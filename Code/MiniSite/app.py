import os
import json
from http.cookies import SimpleCookie

from flask import Flask, render_template, request
app = Flask(__name__)

# define the types of snippets recognized by the app
snippet_types = ["image", "video", "graph", "table", "audio", "infographic", "text"]

# used to store persona preference selections from the user
persona_values = {}

# used to store the calculated affinities that the current user has for each snippet type
snippet_affinities = {}

# read in definitions of the persona definitions
with open('ContentSamples/personas.json') as f:
    persona_definitions = json.load(f)


# read in topic summaries from a theme
with open('ContentSamples/theme.json') as f:
    themes = json.load(f)
    topics = themes[0]['topics']


@app.route("/")
def index():
    # initialize the application from persona preferences stored on the client side
    return render_template("index.html")


@app.route("/theme")
def theme():
    # read in personas
    with open('ContentSamples/personas.json') as f:
        personas = json.load(f)

    # score and sort the topics for display
    return render_template("theme.html", personas=personas, topics=scored_sorted_topics())


@app.route("/topic")
def topic():
    # read in topic details
    id = request.args.get('id')
    with open('ContentSamples/topic_detail.json') as f:
        topic_detail = json.load(f)
        primary_snippets = topic_detail['primary_snippets']
        secondary_snippets = topic_detail['secondary_snippets']

    return render_template("topic.html", primary_snippets=scored_sorted_snippets(primary_snippets), secondary_snippets=scored_sorted_snippets(secondary_snippets))


@app.route("/update-persona")
def updatePersona():
    # store the persona values selected in the user experience
    persona_selections = request.args.get('selections')

    cookie = SimpleCookie()
    cookie.load(persona_selections)

    for key, entry in cookie.items():
        persona_values[key] = entry.value

    print("persona updated: " + str(persona_values))

    # update the individual snippet affinities based on the current persona preferences
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

    for snippet_type in snippet_types:
        snippet_affinities[snippet_type] = snippet_affinity(snippet_type)

    print('snippet affinities: ' + str(snippet_affinities))


def scored_sorted_topics():
    # adds a topic score to each topic in the theme

    # step through the topic summaries in the theme
    for topic_summary in topics:
        # score each of the snippet types in the theme
        topic_score = 0
        for snippet_type in snippet_types:
            try:
                topic_score += topic_summary[snippet_type] * snippet_affinities[snippet_type]
            except:
                # ignore if there are no affinities yet recorded
                pass

        topic_summary['score'] = topic_score

    output_topics = sorted(topics, key=lambda i: i['score'], reverse=True)

    print('scored, sorted topics: ' + str(output_topics))
    return output_topics


def scored_sorted_snippets(snippets):
    # scores and sorts snippets for a topic based on the given snippets and snippet affinities

    # step through each snippet in the list and assign an affinity
    for snippet in snippets:
        snippet['score'] = snippet_affinity(snippet['snippet_type'])

    # return sorted the snippets based on affinity
    return sorted(snippets, key=lambda i: i['score'], reverse=True)


if __name__ == "__main__":
    port = int(os.getenv('PORT'))
    app.run(debug=True, port=port, host='0.0.0.0')

