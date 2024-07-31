from flask import Flask, jsonify
from flask_cors import CORS
import requests
import spacy
from textblob import TextBlob

app = Flask(__name__)
CORS(app)

NEWS_API_KEY = 'ea608dd3d5e140c4a56b37d863d3eb0e'
nlp = spacy.load('en_core_web_sm')

@app.route('/news', methods=['GET'])
def get_news():
    url = "https://newsapi.org/v2/everything"
    querystring = {
        "q": "finance OR investment OR stock OR financial OR trading ",  # Updated query to include multiple keywords
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "relevancy"  # Sort results by relevance
    }
    
    try:
        response = requests.get(url, params=querystring)
        print("Status Code:", response.status_code)
        print("Response URL:", response.url)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to fetch news'}), response.status_code

        response_json = response.json()
        print("Response JSON:", response_json)  # Log the full JSON response

        articles = response_json.get('articles', [])
        print("Number of Articles:", len(articles))  # Log the number of articles

        if not articles:
            print("No articles found")  # Log if no articles are found

        results = []

        for article in articles:
            text = article['title'] + ". " + article['description'] if article['description'] else article['title']
            doc = nlp(text)
            # //below Extract the names of organizations (companies) mentioned in the text:
            companies = [ent.text for ent in doc.ents if ent.label_ == "ORG"]


#             doc.ents gives a list of named entities found in the text.
# ent.label_ == "ORG" filters out entities labeled as organizations.


# //sentiment on overal txt oe and fugured out thee companies out of it
            sentiment = TextBlob(text).sentiment.polarity
            sentiment_label = 'positive' if sentiment > 0 else 'negative' if sentiment < 0 else 'neutral'
            
            results.append({
                'title': article['title'],
                'description': article.get('description', ''),
                'url': article['url'],
                'sentiment': sentiment_label,
                'score': sentiment,
                'companies': companies
            })

        print("Results:", results)  # Log the results before returning

        return jsonify({'articles': results})
    
    except Exception as e:
        print("Error:", str(e))  # Log any exceptions
        return jsonify({'error': 'An error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5003)
