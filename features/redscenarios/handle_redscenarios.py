from .redscenariosdict import redscenarios

import random

def handle_redscenarios():
    scenario = random.choice(redscenarios)
    prompt = scenario["prompt"]
    solution = scenario["solution"]
    response = f"**Here's a Red Team Scenario for you**:\n\n**Prompt**: {prompt}\n\n**Solution**: ||{solution}||"
    return response
