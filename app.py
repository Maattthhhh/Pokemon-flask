import os
import re
import requests
from bs4 import BeautifulSoup as soup
from urllib.parse import quote
from flask import Flask, render_template, send_from_directory, jsonify, request

my_email = os.getenv("MY_SCRAPER_EMAIL", "satoshi.kon.fanboy@gmail.com")
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_pokemon')
def get_pokemon():
    AD = request.args.get('pokemonName')
    my_url = "https://pokemondb.net/pokedex/" + AD
    headers = {
        "User-Agent": "Maattthhhh ({my_email}) Python-requests"
    }
    try:
        response = requests.get(my_url, headers=headers)
        if response.status_code != 200:
            return jsonify(cleaned_text=f"Could not find a page for {my_url}!")
        page_soup = soup(response.content, "html.parser")
        paragraphs = page_soup.findAll('p')
        filter_phrases = ["was the", "is the", "are the", "was a", "is a", "are a"]
        cleaned_text = ""

        for p in paragraphs:
            paragraph_text = p.get_text().lower()
            if any(phrase in paragraph_text for phrase in filter_phrases):
                text_with_notations = p.get_text()
                cleaned_text = re.sub(r'\[\d+\]', '', text_with_notations)
                print()
                print(cleaned_text)
                print()
        return jsonify(cleaned_text=cleaned_text)
    except Exception as e:
        return jsonify(cleaned_text=f"An error occurred: {str(e)}")

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)