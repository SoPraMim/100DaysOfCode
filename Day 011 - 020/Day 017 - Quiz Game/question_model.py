class Question:
    
    def __init__(self, question, answer) -> None:
        if not isinstance(question, str):
            raise TypeError("Only strings are allowed for the answer.")
        if not isinstance(answer, str):
            raise TypeError("Only strings are allowed for the answer.")
        self.question = question
        self.answer = answer