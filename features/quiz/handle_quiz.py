import random

from .quizdict import quizdict

def handle_quiz():
    random.shuffle(quizdict)
    question = random.choice(quizdict)
    prompt = question["question"]
    answer = question["answer"]
    response = f"**Here's a security question for you**:\n\n**Prompt**: {prompt}\n\n**Answer**: ||{answer}||"
    return response
