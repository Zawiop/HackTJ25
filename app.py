from flask import Flask, render_template, jsonify, request
from google import genai

app = Flask(__name__)

class AkinatorCareer:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.chat = self.client.chats.create(model="gemini-2.0-flash")
        # This list will hold the full conversation history.
        self.history = []
        self.orig_prompt = (
            "You are an AI playing a career-matching game in an akinator style to assign the user a career "
            "based on their personality/hobbies. You will ask a series of free-response questions to narrow "
            "down the user's career. Each question should be refined based on previous responses. Ask questions "
            "that let the user explain their thoughts briefly and clearly. Keep all questions and responses SIMPLE and to the point. "
            "The goal is to match the user to their ideal career, so don't ask the user directly what their career is, as they aren't sure either.\nQuestions:\nAnswers:"
        )
        # Initialize the conversation history with the original prompt.
        self.history.append(self.orig_prompt)
        # Force the AI to produce a first question right away.
        self.send_message("Ask your first question expecting a free response answer.")

    def send_message(self, message, add_to_history=True):
        """
        Appends the new message to the conversation (if desired), sends the full conversation
        to the AI, and returns the AI's response text.
        """
        if add_to_history:
            self.history.append(message)
        # Concatenate the conversation history into one prompt.
        full_prompt = "\n".join(self.history)
        ai_response = self.chat.send_message(full_prompt)
        response_text = ai_response.text.strip()
        # Append the AI's response to the conversation history.
        self.history.append(response_text)
        return response_text

# Create a global instance of the career-guessing AI.
api_key = "AIzaSyDzGSAgR6R7T6T0PJeMy6xCuPCVFdHtXHA"  # Replace with your actual API key.
akinator = AkinatorCareer(api_key)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_initial_question', methods=['GET'])
def get_initial_question():
    """
    Returns the first AI-generated question (the last entry in history),
    which was produced in AkinatorCareer.__init__.
    """
    first_question = akinator.history[-1]
    is_final = ("your career is" in first_question.lower() or "finish" in first_question.lower())
    return jsonify({'question': first_question, 'is_final': is_final})

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    user_answer = data.get('answer', '').strip()
    
    # Only append the user's answer if it's not empty.
    if user_answer:
        _ = akinator.send_message(f"My answer is: {user_answer}")
    
    # Re-prompt the AI with the full conversation history plus an instruction to continue.
    next_question = akinator.send_message(
        "Continue the conversation. Based on all previous questions and responses, ask the next question expecting a free response answer. Always provide a question unless you have determined the user's ideal career. Keep it simple and to the point."
    )
    
    # Determine if the AI indicates that the game is over.
    is_final = ("your career is" in next_question.lower() or "finish" in next_question.lower())
    
    return jsonify({'question': next_question, 'is_final': is_final})

if __name__ == '__main__':
    app.run(debug=True)
