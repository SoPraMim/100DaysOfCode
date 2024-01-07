from question_model import Question
from data import question_data
from quiz_brain import QuizBrain

question_bank=[]
for item in question_data["results"]:
    question = Question(item["question"], item["correct_answer"])
    question_bank.append(question)

quiz = QuizBrain(question_bank)

while quiz.still_has_questions():
    answer = quiz.next_question()
    quiz.check_answer(answer)
    
print("You've completed the quiz.")
print(f"Your final score was {quiz.score}/{quiz.question_number}")