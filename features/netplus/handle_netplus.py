import random

from .netplusdict import netplusdict

def handle_netplus():
    random.shuffle(netplusdict)
    question = random.choice(netplusdict)
    prompt = question["question"]
    answer = question["answer"]
    response = f"**Here's a practice Network+ question for you**:\n\n**Prompt**: {prompt}\n\n**Answer**: ||{answer}||"
    return response
