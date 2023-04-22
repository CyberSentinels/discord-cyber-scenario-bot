import os

from features.cissp.handle_cissp import cisspdict
from features.ccna.handle_ccna import ccnadict
from features.ceh.handle_ceh import cehdict
from features.aplus.handle_aplus import aplusdict
from features.netplus.handle_netplus import netplusdict
from features.linuxplus.handle_linuxplus import linuxplusdict
from features.secplus.handle_secplus import secplusdict
from features.quiz.handle_quiz import quizdict

VALID_QUIZ_EMOJIS = ["🇦", "🇧", "🇨", "🇩", "❓"]
EMOJI_TO_ANSWER = {
    "🇦": "A",
    "🇧": "B",
    "🇨": "C",
    "🇩": "D",
    "❓": "show_answer"
}
guildid = os.environ.get("GUILD_ID")

user_responses = {}  # Format: {message_id: {question_id: {user_id: answer}}}
user_scores = {}     # Format: {user_id: {quiz_id: {correct: int, incorrect: int }}}


async def handle_quiz_reaction(react, user, client):
    if user == client.user or react.message.author != client.user:
        return

    if is_valid_quiz_emoji(react.emoji):
        msg_id = react.msg_id
        question_id = react.message.embeds[0].footer.text
        user_id = str(user.id)

        if user_already_reacted(msg_id, question_id, user_id):
            await react.remove(user)
            return

        add_user_response(react, user, client)

        await react.remove(user)

        response_str = create_response_str(
            quiz_id, question_number, user_answer)

        await user.send(response_str)


def is_valid_quiz_emoji(emoji):
    VALID_QUIZ_EMOJIS = ["🇦", "🇧", "🇨", "🇩", "❓"]
    return emoji in VALID_QUIZ_EMOJIS


def user_already_reacted(user_id, msg_id, question_id):
    return msg_id in user_responses and question_id in user_responses[msg_id] and user_id in user_responses[msg_id][question_id]


def add_user_response(msg_id, question_id, user_id, user_answer):
    if msg_id not in user_responses:
        user_responses[msg_id] = {}
    if question_id not in user_responses[msg_id]:
        user_responses[msg_id][question_id] = {}
        user_responses[msg_id][question_id][user_id] = user_answer


def create_response_str(user_id, quiz_id, question_number, user_answer):
    QUESTION_DICT_MAPPING = {
        "cissp": cisspdict,
        "ceh": cehdict,
        "ccna": ccnadict,
        "aplus": aplusdict,
        "netplus": netplusdict,
        "linuxplus": linuxplusdict,
        "secplus": secplusdict,
        "quiz": quizdict
        # Add more prefixes and corresponding question dictionaries as needed
    }
    question_dict = QUESTION_DICT_MAPPING[quiz_id]
    question = question_dict[question_number]
    correct_answer = question["correctanswer"].lower()
    ans = user_answer.lower()
    if ans == "show_answer":
        return create_show_answer_str(correct_answer, question, "reasoning" in question)

    if user_id not in user_scores:
        user_scores[user_id] = {
            p: {"correct": 0, "incorrect": 0} for p in QUESTION_DICT_MAPPING}

    if ans == correct_answer:
        return create_correct_answer_str(
            user_answer, question, "reasoning" in question)
    else:
        return create_incorrect_answer_str(
            user_answer, correct_answer, question, "reasoning" in question
        )


def create_show_answer_str(correct_answer, question, with_reasoning):
    if with_reasoning:
        return f"The correct answer is '{correct_answer}'\n\n**Reasoning**: {question['reasoning']}"
    else:
        return f"The correct answer is '{correct_answer}'"


def create_correct_answer_str(user_answer, question, with_reasoning):
    if with_reasoning:
        return f"🎉 Congratulations, your answer '{user_answer}' is correct!\n\n**Reasoning**: {question['reasoning']}"
    else:
        return f"🎉 Congratulations, your answer '{user_answer}' is correct!"


def create_incorrect_answer_str(user_answer, correct_answer, question, with_reasoning):
    if with_reasoning:
        return f"🤔 Your answer '{user_answer}' is incorrect. The correct answer is '{correct_answer}'.\n\n**Reasoning**: {question['reasoning']}"
    else:
        return f"🤔 Your answer '{user_answer}' is incorrect. The correct answer is '{correct_answer}'."


# def get_members(client, reaction, guildid):
#     guild = client.get_guild(guildid) or reaction.message.guild
#     if guild is None:
#         raise Exception(
#             f"Warning: Unable to find a guild with the ID {guildid}")
#     return guild.members
