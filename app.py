import os
from flask import Flask, request
from google import genai

app = Flask(__name__)

# السيرفر سيقرأ المفتاح من إعداداته الداخلية بأمان دون كشفه في الكود
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

@app.route("/", methods=["GET", "POST"])
def home():
    user_input = ""
    ai_response = ""
    
    if request.method == "POST":
        user_input = request.form.get("user_message", "")
        
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_input,
            )
            ai_response = response.text
        except Exception as e:
            ai_response = f"Connection Error: {str(e)}"

    return f"""
    <html>
        <head>
            <title>AI Smart Research Hub</title>
            <style>
                body {{ font-family: sans-serif; margin: 50px auto; max-width: 700px; background-color: #0f172a; color: #f8fafc; padding: 20px; }}
                .chat-box {{ background-color: #1e293b; padding: 25px; border-radius: 12px; }}
                textarea {{ width: 100%; height: 120px; padding: 12px; background-color: #0f172a; color: white; border: 1px solid #38bdf8; border-radius: 8px; resize: none; }}
                input[type="submit"] {{ margin-top: 15px; padding: 12px 24px; background-color: #38bdf8; color: #0f172a; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; }}
                .response-area {{ margin-top: 30px; padding: 20px; background-color: #0f172a; border-left: 4px solid #4ade80; border-radius: 4px; text-align: left; white-space: pre-wrap; }}
            </style>
        </head>
        <body>
            <div class="chat-box">
                <h1>AI Research Assistant</h1>
                <form method="POST">
                    <textarea name="user_message" placeholder="Type your question here...">{user_input}</textarea>
                    <input type="submit" value="Ask AI">
                </form>
                {f'<div class="response-area"><strong>AI Response:</strong><br><br>{ai_response}</div>' if ai_response else ''}
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)
