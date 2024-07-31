from flask import Flask, request, jsonify
from Gemini import geminiApp
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

@app.route('/output', methods=['POST'])
def handlePrompt():
    data = request.get_json()

    if 'prompt' not in data:
        return jsonify({'error': 'Prompt parameter is missing'}), 400
    
    prompt = data['prompt']

    # Call geminiApp function to get response from Gemini AI
    response = geminiApp(prompt)

    return jsonify({
        'prompt': prompt,
        'output': response
    })

if __name__ == '__main__':
    app.run(debug=True,port=5001)
