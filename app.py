from flask import Flask, render_template, jsonify, request
from google import genai

app = Flask(__name__)

class AkinatorCareer:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.chat = self.client.chats.create(model="gemini-2.0-flash")
        self.orig_prompt = (
            "You are an AI playing a career-matching game in an akinator style to assign the user a career based on their personality/hobbies."
            " You will ask a series of yes/no/maybe to narrow down the user's career."
            " Each question should be refined based on previous responses."
            " Format each question with multiple-choice options."
            " Keep all questions/responses short and to the point."
            " The goal is to match the user to their ideal career, so don't try and ask the user their career, as they aren't sure either."
            "\nQuestions:\nAnswers:"
        )
        # Start the conversation with the original prompt.
        self.send_message(self.orig_prompt)

    def send_message(self, message):
        """Sends a message to the AI and returns the response text."""
        ai_response = self.chat.send_message(message)
        return ai_response.text.strip()

# Create a global instance of the career-guessing AI.
api_key = "AIzaSyDzGSAgR6R7T6T0PJeMy6xCuPCVFdHtXHA"  # Replace with your actual API key.
akinator = AkinatorCareer(api_key)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    user_answer = data.get('answer', '')
    
    # Append the user's answer into the conversation.
    _ = akinator.send_message(f"My answer is: {user_answer}")
    
    # Ask the AI for the next question.
    next_question = akinator.send_message("Ask the next question with multiple-choice options.")
    
    # Determine if the AI indicates that the game is over.
    is_final = ("your career is" in next_question.lower() or "finish" in next_question.lower())
    
    return jsonify({'question': next_question, 'is_final': is_final})

if __name__ == '__main__':
    app.run(debug=True)
