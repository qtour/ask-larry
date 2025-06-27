from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/')
def root():
    return send_from_directory('.', 'ask-larry.html')

@app.route('/<path:filename>')
def static_file(filename):
    return send_from_directory('.', filename)

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
