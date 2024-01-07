class QuizBrain:
    
    def __init__(self, question_list):
        if not isinstance(question_list,list):
            raise TypeError("question:list should be a list of Question objects.")
               
        self.question_number = 0
        self.question_list = question_list
        self.score = 0
    
    def next_question(self):
        current_question = self.question_number
        while True:
            answer = input(f"Q.{current_question+1}: {self.question_list[current_question].question} (True/False)? ").lower()
            if answer in ["true","false"]:
                return answer
            else:
                print("Wrong input. Please try again.")
        
    def still_has_questions(self):
        return self.question_number < len(self.question_list)
    
    def check_answer(self, answer):
        
        answer = answer.lower()
        
        question = self.question_list[self.question_number]
        correct_answer = question.answer.lower()
        self.question_number += 1
        if answer == correct_answer:
            self.score += 1
            print("You got it right!")
        else:
            print(f"You got it wrong. The correct answer was {correct_answer}.")
        print(f"Your current score is: {self.score} / {self.question_number}")
        print("\n")
        
