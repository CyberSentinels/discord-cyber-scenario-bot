import random

from .cisspdict import cisspdict


import random

def handle_cissp(user_responses):
    # Create a list of question IDs, weighted based on user responses
    weighted_question_ids = []
    for i, question in enumerate(cisspdict):
        # Get the question ID and correct answer
        prefix = "cissp_"  # Unique prefix for CISSP questions
        question_id = prefix + str(i)
        correct_answer = question["correctanswer"]

        # Compute the weight based on user responses
        weight = 1
        if question_id in user_responses:
            user_answer = user_responses[question_id]
            if user_answer != correct_answer:
                weight += 1  # Increase weight for incorrect answers
            else:
                weight -= 1  # Decrease weight for correct answers

        # Add the question ID to the list with the appropriate weight
        weighted_question_ids.extend([question_id] * weight)

    # Select a random question ID from the weighted list
    question_id = random.choice(weighted_question_ids)

    # Retrieve the selected question
    question = cisspdict[int(question_id)]
    prompt = question["question"]
    answers = question["answers"]
    correct_answer = question["correctanswer"]
    reasoning = question["reasoning"] or None

    # Format the response
    options = []
    for key, value in answers.items():
        if key != "correctanswer":
            options.append(f"**{key.upper()}**: {value}")
    options = "\n".join(options)
    if reasoning is not None:
        response = f"**Here's a CISSP question for you**:\n\n**Question**: {prompt}\n\n**Options**: \n{options}\n\n**Correct Answer**: ||{correct_answer}||\n\n**Reasoning**: ||{reasoning}||"
    else:
        response = f"**Here's a CISSP question for you**:\n\n**Question**: {prompt}\n\n**Options**: \n{options}\n\n**Correct Answer**: ||{correct_answer}||"

    return response, question_id
