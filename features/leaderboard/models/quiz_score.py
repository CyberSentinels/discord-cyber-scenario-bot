class QuizScore:
    def __init__(self, quiz_id):
        self.quiz_id = quiz_id
        self.correct = 0
        self.incorrect = 0

    def inc_correct(self):
        self.correct += 1
    
    def inc_incorrect(self):
        self.incorrect += 1
