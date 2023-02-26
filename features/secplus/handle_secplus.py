from .secplusdict import secplusdict
import random

def handle_secplus():
    question = random.choice(secplusdict)
    prompt = question["question"]
    answer = question["answer"]
    response = f"**Here's a practice Security+ question for you**:\n\n**Prompt**: {prompt}\n\n**Answer**: ||{answer}||"
    return response
