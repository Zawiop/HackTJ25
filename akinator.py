from google import genai

class AkinatorCareer:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.chat = self.client.chats.create(model="gemini-2.0-flash")
        self.orig_prompt = (
            "You are an AI playing a career-guessing game in an akinator style."
            " You will ask a series of yes/no or multiple-choice questions to narrow down the user's career."
            " Each question should be refined based on previous responses."
            " Format each question with multiple-choice options."
            "\nQuestions:\nAnswers:"
        )
        self.send_message(self.orig_prompt)

    def send_message(self, message):
        """Sends a message to the AI and returns the response."""
        ai_response = self.chat.send_message(message)
        return ai_response.text.strip()

    def start_game(self):
        """Begins the interactive question loop."""
        while True:
            ai_question = self.send_message("Ask the next question with multiple-choice options.")
            print("\n" + ai_question)

            # Extract and display multiple-choice options
            options = self.extract_options(ai_question)
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")

            # User selects an answer
            choice = self.get_user_choice(len(options))

            # Send selected answer to AI
            response = self.send_message(f"My answer is: {options[choice - 1]}")

            # If AI determines a career or ends the game, break loop
            if "your career is" in response.lower() or "finish" in response.lower():
                print("\n" + response)
                break

    def extract_options(self, text):
        """Extracts multiple-choice options from AI-generated questions."""
        lines = text.split("\n")
        options = [line.strip() for line in lines if line.strip() and not line.endswith("?")]
        return options if options else ["Yes", "No"]  # Default to Yes/No if no options are given

    def get_user_choice(self, num_options):
        """Gets a valid user selection from multiple-choice options."""
        while True:
            try:
                choice = int(input("Select an option (number): "))
                if 1 <= choice <= num_options:
                    return choice
                else:
                    print("Invalid choice. Please select a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

# Initialize and start the game
api_key = "AIzaSyDzGSAgR6R7T6T0PJeMy6xCuPCVFdHtXHA"
akinator = AkinatorCareer(api_key)
akinator.start_game()
