import random

from .ccnadict import ccnadict


import random

def handle_ccna():
    question = random.choice(ccna)
    prompt = question["question"]
    answers = question["answers"]
    options = []
    for key, value in answers.items():
        if key != "correctanswer":
            options.append(f"{key}. {value}")
    options = "\n".join(options)
    correct_answer = answers["correctanswer"]
    response = f"**Here's a CCNA question for you**:\n\n**Question**: {prompt}\n\n**Options**: {options}\n\n**Correct Answer**: ||{correct_answer}||"
    return response
