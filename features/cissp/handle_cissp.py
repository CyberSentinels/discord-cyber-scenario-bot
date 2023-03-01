import random

from .cisspdict import cisspdict


import random

def handle_cissp():
    question = random.choice(cisspdict)
    prompt = question["question"]
    answers = question["answers"]
    correctanswer = question["correctanswer"]
    reasoning = question["reasoning"] or None
    options = []
    for key, value in answers.items():
        if key != "correctanswer":
            options.append(f"**{key.upper()}**: {value}")
    options = "\n".join(options)
    correct_answer = answers["correctanswer"]
    if "reasoning" is not None:
        response = f"**Here's a CISSP question for you**:\n\n**Question**: {prompt}\n\n**Options**: \n{options}\n\n**Correct Answer**: ||{correct_answer}||\n\n**Reasoning**: ||{reasoning}||"
    else:
        response = f"**Here's a CISSP question for you**:\n\n**Question**: {prompt}\n\n**Options**: \n{options}\n\n**Correct Answer**: ||{correct_answer}||"
    return response