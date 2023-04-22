class UserQuizResponses:
    def __init__(self):
        self.responses = {}

    def add_response(self, message_id, question_id, user_id, answer):
        if message_id not in self.responses:
            self.responses[message_id] = {}
        if question_id not in self.responses[message_id]:
            self.responses[message_id][question_id] = {}
        self.responses[message_id][question_id][user_id] = answer

    def already_answered(self, message_id, question_id, user_id):
        return message_id in self.responses and question_id in self.responses[message_id] and user_id in self.responses[message_id][question_id]
