from flask import Flask, request, jsonify
from flask_cors import CORS
import pytesseract
from PIL import Image
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        image = Image.open(filepath)
        raw_text = pytesseract.image_to_string(image)
        clean_text = raw_text.strip().replace('\n', ' ')

        larry_response = f"Alright, let's look at this: '{clean_text}'\nHere's how we'd tackle it step by step... (This is where Larry's explanation will go)"
        return jsonify({'question': clean_text, 'larry_response': larry_response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ask', methods=['POST'])
def ask_larry():
    data = request.get_json()
    question = data.get('question', '')

    if not question:
        return jsonify({'response': 'No question received.'})

    try:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are Larry, a warm, practical, non-judgmental Irish tradesman turned math tutor. "
                    "Explain things simply and clearly using metric units only. Be friendly and encouraging."
                )
            },
            {"role": "user", "content": question}
        ]

        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7
        )

        answer = response.choices[0].message.content.strip()
        return jsonify({'response': answer})

    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
