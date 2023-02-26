
from ..bluescenarios.bluescenariosdict import bluescenarios
from ..redscenarios.redscenariosdict import redscenarios
import random

def handle_scenarios():
    scenarios = bluescenarios + redscenarios
    scenario = random.choice(scenarios)
    prompt = scenario["prompt"]
    if "ways_to_prevent" in scenario:
        prevent = "\n".join(scenario["ways_to_prevent"])
        respond = "\n".join(scenario["how_to_respond"])
        response = f"**Here's a Blue Team Scenario for you**:\n\nPrompt: {prompt}\n\n**Ways to prevent**: ||{prevent}||\n\n**How to respond**: ||{respond}||"
    else:
        solution = scenario["solution"]
        response = f"**Here's a Red Team Scenario for you**:\n\n**Prompt**: {prompt}\n\n**Solution**: ||{solution}||"