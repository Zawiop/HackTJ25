from flask import Flask, render_template, request, jsonify
import google.genai as genai

app = Flask(__name__)

class AkinatorCareer:
    def __init__(self, api_key):
        # Initialize the Google GenAI client
        self.client = genai.Client(api_key=api_key)
        # Create a chat session with a chosen model
        self.chat = self.client.chats.create(model="gemini-2.0-flash")
        self.history = []
        
        # A general introduction or “system” prompt
        self.intro_prompt = (
            "You are an AI playing a career-matching game in an Akinator style. "
            "Ask the user a series of open-ended questions to figure out an ideal career. "
            "Keep questions short, free-response, and refine them based on prior answers. "
            "Don’t just ask for their desired career directly; lead them to it. "
            "When you are certain, reveal the user's ideal career in a single statement."
        )
        self.history.append(self.intro_prompt)

        # Ask for the first question right away
        self.get_next_question("Please ask your first question now, expecting a free-response answer.")

    def get_next_question(self, prompt):
        """
        Sends a prompt to the model and updates history with the response.
        """
        self.history.append(prompt)
        full_prompt = "\n".join(self.history)
        response = self.chat.send_message(full_prompt)
        answer = response.text.strip()
        self.history.append(answer)
        return answer

    def user_answered(self, user_text):
        """
        Incorporates the user's answer, then asks the model to proceed.
        """
        if user_text:
            # Append user’s answer
            self.history.append(f"My answer is: {user_text}")
        # Prompt the model for the next question or final result
        next_step = "Please ask the next question unless you're ready to provide the final career."
        return self.get_next_question(next_step)

# Create a global instance of the AkinatorCareer
# (Replace with your actual API key)
global_akinator = AkinatorCareer(api_key="AIzaSyDzGSAgR6R7T6T0PJeMy6xCuPCVFdHtXHA")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_initial_question', methods=['GET'])
def get_initial_question():
    """
    Returns the last message from the AI, which should be the first question.
    """
    last_message = global_akinator.history[-1]
    final_check = "your career is" in last_message.lower() or "finish" in last_message.lower()
    return jsonify({'question': last_message, 'is_final': final_check})

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    """
    Receives the user's answer, sends it to the AI, and returns the AI's next question or final answer.
    """
    data = request.get_json()
    user_text = data.get('answer', '').strip()
    
    # Pass the user's text to the conversation manager
    new_response = global_akinator.user_answered(user_text)
    
    # Check if the AI is providing a final result
    final_check = "your career is" in new_response.lower() or "finish" in new_response.lower()
    return jsonify({'question': new_response, 'is_final': final_check})

if __name__ == '__main__':
    app.run(debug=True)
