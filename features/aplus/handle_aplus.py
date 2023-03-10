import random

from .aplusdict import aplusdict

def handle_aplus():
    random.shuffle(aplusdict)
    question = random.choice(aplusdict)
    prompt = question["question"]
    answer = question["answer"]
    response = f"**Here's a practice A+ question for you**:\n\n**Prompt**: {prompt}\n\n**Answer**: ||{answer}||"
    return response
