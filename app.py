import re
import requests
import json
from bs4 import BeautifulSoup as soup
from urllib.parse import quote
from flask import Flask, request, render_template, send_from_directory
from flask import jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_pokemon')
def get_pokemon():
    AD = request.args.get('pokemonName')
    my_url = "https://pokemon.fandom.com/wiki/" + AD
    response = requests.get(my_url)
    if response.status_code == 200:
        page_soup = soup(response.content, "html.parser")
        paragraphs = page_soup.findAll('p')
        filter_phrases = ["was the", "is the", "are the", "was a", "is a", "are a"]

        for p in paragraphs:
            paragraph_text = p.get_text().lower()
            if any(phrase in paragraph_text for phrase in filter_phrases):
                text_with_notations = p.get_text()
                cleaned_text = re.sub(r'\[\d+\]', '', text_with_notations)
                print()
                print(cleaned_text)
                print()
    return jsonify({'cleaned_text': cleaned_text})

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)