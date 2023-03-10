import random

from .bluescenariosdict import bluescenarios

def handle_bluescenarios():
    random.shuffle(bluescenarios)
    scenario = random.choice(bluescenarios)
    prompt = scenario["prompt"]
    prevent = "\n".join(scenario["ways_to_prevent"])
    respond = "\n".join(scenario["how_to_respond"])
    response = f"**Here's a Blue Team Scenario for you**:\n\n**Prompt**: {prompt}\n\n**Ways to prevent**: ||{prevent}||\n\n**How to respond**: ||{respond}||"
    return response
