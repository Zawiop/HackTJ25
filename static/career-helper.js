document.getElementById('nextBtn').addEventListener('click', getNextQuestion);

function getNextQuestion() {
  fetch('/get_question')
    .then(response => response.json())
    .then(data => {
      const questionElement = document.getElementById('question');
      const questionText = data.question;
      if (data.is_final) {
        questionElement.textContent = "Final Answer: " + questionText;
        document.getElementById('nextBtn').disabled = true;
      } else {
        questionElement.textContent = questionText;
      }
    })
    .catch(error => console.error('Error fetching question:', error));
}
