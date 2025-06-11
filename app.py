from flask import Flask, request, jsonify, send_file
import os
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return send_file("ask-larry.html")

@app.route("/ask-larry", methods=["POST"])
def ask_larry():
    data = request.get_json()
    question = data.get("question", "")

    prompt = f"""
You are 'Larry', a cabinet maker turned psychology graduate who helps young adults in the trades with practical maths.
You're Irish, warm, non-condescending, and explain things clearly using the metric system only.
Keep answers short, visual if needed, and tied to practical, on-the-job scenarios.

Here's the question: {question}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are Ask Larry, a helpful maths tutor for apprentices."},
                {"role": "user", "content": prompt}
            ]
        )
        return jsonify({"reply": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"Oops! Larry ran into a problem: {str(e)}"}), 500
