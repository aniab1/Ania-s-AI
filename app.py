import os
from flask import Flask, request, jsonify, render_template_string
from google import genai
from google.genai import types

app = Flask(__name__)

# إعداد العميل باستخدام مفتاح البيئة السرية
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# واجهة المستخدم (HTML + CSS مريح للعين)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ania-s-AI | النسخة المتقدمة</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121214; color: #e2e8f0; max-width: 800px; margin: 0 auto; padding: 20px; }
        .chat-container { background: #1a1a1e; border-radius: 12px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); min-height: 400px; display: flex; flex-direction: column; justify-content: space-between; }
        #chat-box { flex-grow: 1; overflow-y: auto; margin-bottom: 20px; border-bottom: 1px solid #2d2d34; padding-bottom: 10px; }
        .message { margin: 10px 0; padding: 12px; border-radius: 8px; line-height: 1.6; }
        .user-msg { background: #2b6cb0; color: white; align-self: flex-start; }
        .ai-msg { background: #2d2d34; border-left: 4px solid #48bb78; }
        .input-area { display: flex; gap: 10px; }
        input { flex-grow: 1; padding: 12px; border: 1px solid #4a5568; background: #2d2d34; color: white; border-radius: 6px; }
        button { padding: 12px 24px; background: #48bb78; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; }
        button:hover { background: #38a169; }
    </style>
</head>
<body>
    <h2>المساعد الذكي المتطور لعقول الفيزياء والمنطق 🌌</h2>
    <div class="chat-container">
        <div id="chat-box"></div>
        <div class="input-area">
            <input type="text" id="user-input" placeholder="اطرح سؤالك العميق هنا...">
            <button onclick="sendMessage()">إرسال</button>
        </div>
    </div>

    <script>
        async function sendMessage() {
            const inputDel = document.getElementById('user-input');
            const message = inputDel.value.trim();
            if(!message) return;
            
            const chatBox = document.getElementById('chat-box');
            chatBox.innerHTML += `<div class="message user-msg"><b>أنتِ:</b> ${message}</div>`;
            inputDel.value = '';

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ message: message })
                });
                const data = await response.json();
                chatBox.innerHTML += `<div class="message ai-msg"><b>الذكاء الاصطناعي:</b> ${data.reply}</div>`;
            } catch (error) {
                chatBox.innerHTML += `<div class="message ai-msg" style="color:red;">خطأ في الاتصال بالسيرفر!</div>`;
            }
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    # هنا تكمن السرعة والذكاء والتعليمات الصارمة للشخصية!
    system_instruction = (
        "أنت مساعد ذكاء اصطناعي فائق الذكاء، صُممت خصيصاً لخدمة العقول النخبوية التي تعشق الفيزياء النظرية والرياضيات والمنطق البنيوي. "
        "أسلوبك عميق، دقيق، ومباشر. تجنب السطحية تماماً أو الأجوبة الجاهزة المكررة. "
        "عند شرح أي مفهوم علمي، ركز على 'البرهان المنطقي' و'الفكرة المفاهمية الهيكلية' بدلاً من الحفظ أو التلقين. "
        "تحدث بذكاء حاد، وكن دائماً مستعداً لتحليل النظريات المتقدمة مثل ميكانيكا الكم، والنسبية، والشبكات العصبية الفيزيائية بثقة وعمق يفوق أي مساعد آخر."
    )
    
    try:
        response = client.models.generate_content(
            model='gemini-1.5-pro',  # الترقية للنموذج الأقوى والأعمق
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3
            )
        )
        reply = response.text
    except Exception as e:
        reply = f"حدث خطأ أثناء معالجة الفكرة منطقياً: {str(e)}"
        
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000) 
