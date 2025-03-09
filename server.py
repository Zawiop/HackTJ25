from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

questions = [
    "What type of career are you interested in?",
    "Do you enjoy working with technology?",
    "Are you looking for a job in healthcare?",
    "What is your preferred work environment?",
    "Would you like a job that involves travel?"
]

@app.route('/')
def home():
    # This serves index.html from the templates/ folder
    return render_template('index.html')

@app.route('/get_question')
def get_question():
    question = random.choice(questions)
    is_final = "job" in question.lower()
    return jsonify({'question': question, 'is_final': is_final})

if __name__ == '__main__':
    app.run(debug=True)
