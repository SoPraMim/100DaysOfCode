import requests
import html

class QuizBrain:
    def __init__(self):
        self.question_number = 0
        self.score = 0
        self.question_list = None
        self.current_question = None
        self.get_questions()

    def get_questions(self):
        parameters = {
            "amount":10,
            "type":"boolean"
        }       
        response = requests.get(url="https://opentdb.com/api.php",params=parameters)
        response.raise_for_status()
        question_data = response.json()["results"]
        question_bank = [Question(html.unescape(question["question"]),question["correct_answer"]) for question in question_data]
        self.question_list = question_bank

    def still_has_questions(self) -> bool:
        return self.question_number < len(self.question_list)

    def next_question(self) -> str:
        self.current_question = self.question_list[self.question_number]
        self.question_number += 1
        return f"Q.{self.question_number}: {self.current_question.text}"

    def check_answer(self, user_answer: bool) -> bool:
        correct_answer = self.current_question.answer
        if user_answer == correct_answer:
            self.score += 1
            return True
        else:
            return False


class Question:

    def __init__(self, q_text: str, q_answer: str):
        self.text = q_text
        if q_answer.lower() == "true":
            self.answer = True
        elif q_answer.lower() == "false":
            self.answer = False
