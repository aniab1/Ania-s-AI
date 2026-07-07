from flask import Flask, render_template, request, jsonify
from google import genai
import os

app = Flask(__name__)

# Initialize the Gemini Client
# It automatically picks up the GEMINI_API_KEY environment variable from Render
client = genai.Client()

@app.route('/')
def index():
    # This renders the main interface
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')

        # Corrected model name for google-genai
        response = client.models.generate_content(
            model="gemini-1.5-pro",
            contents=user_message
        )
        
        return jsonify({"reply": response.text})

    except Exception as e:
        # English error message
        error_message = f"An error occurred during logical processing: {str(e)}"
        return jsonify({"reply": error_message})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000) 
