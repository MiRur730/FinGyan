from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)

# Configure CORS
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins, adjust as needed

RAPIDAPI_KEY = '4f00659f6cmsh4fdf4cf18628e53p192c98jsnca4112a70b61'
RAPIDAPI_HOST = 'dailymotion-video-information-api.p.rapidapi.com'

# List of finance-related terms
FINANCE_TERMS = ['finance', 'investment', 'stock', 'economy', 'financial', 'trading', 'business']

@app.route('/dailymotion', methods=['POST'])
def get_videos():
    data = request.get_json()
    if 'keywords' not in data:
        return jsonify({'error': 'Keywords parameter is missing'}), 400

    keywords = data['keywords']
    response = requests.get(
        
        f'https://api.dailymotion.com/videos?search={keywords}&fields=id,title,thumbnail_360_url,embed_url',
        headers={
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': RAPIDAPI_HOST,
        }
    )

    if response.status_code == 200:
        videos = response.json().get('list', [])

        # Filter videos to only include those related to finance
        def is_finance_related(text):
            text = text.lower()
            return any(term in text for term in FINANCE_TERMS)

        finance_related_videos = [video for video in videos if is_finance_related(video['title']) or is_finance_related(video.get('description', ''))]

        return jsonify({
            'keywords': keywords,
            'videos': [{'url': video['embed_url'], 'title': video['title'], 'thumbnail': video['thumbnail_360_url']} for video in finance_related_videos]
        })
    else:
        return jsonify({'error': 'Failed to fetch videos'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True, port=5002)
