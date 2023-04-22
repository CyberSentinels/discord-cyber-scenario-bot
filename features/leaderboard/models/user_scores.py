from features.leaderboard.models.quiz_score import QuizScore


class UserScores:
    def __init__(self):
        self.quiz_scores = {}

    def handle_quiz_answer(self, user_id, quiz_id, is_correct):
        if user_id not in self.scores:
            self.quiz_scores[user_id] = {
                quiz_id: QuizScore(quiz_id)
            }
            self.quiz_scores[quiz_id] = QuizScore(quiz_id)

        if is_correct:
            self.quiz_scores[quiz_id].inc_correct()
        else:
            self.quiz_scores[quiz_id].inc_incorrect()
