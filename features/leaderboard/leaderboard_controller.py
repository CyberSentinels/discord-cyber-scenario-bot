import os

from features.leaderboard.models.user_responses import UserQuizResponses

from features.cissp.handle_cissp import cisspdict
from features.ccna.handle_ccna import ccnadict
from features.ceh.handle_ceh import cehdict
from features.aplus.handle_aplus import aplusdict
from features.leaderboard.models.user_scores import UserScores
from features.netplus.handle_netplus import netplusdict
from features.linuxplus.handle_linuxplus import linuxplusdict
from features.secplus.handle_secplus import secplusdict
from features.quiz.handle_quiz import quizdict

user_quiz_responses = UserQuizResponses()
user_scores = UserScores()

VALID_QUIZ_EMOJIS = ["🇦", "🇧", "🇨", "🇩", "❓"]
EMOJI_TO_ANSWER = {
    "🇦": "A",
    "🇧": "B",
    "🇨": "C",
    "🇩": "D",
    "❓": "show_answer"
}
guildid = os.environ.get("GUILD_ID")

question_dict_mapping = {
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


async def handle_quiz_reaction(react, user, client):
    if user == client.user or react.message.author != client.user:
        return

    if react.emoji in VALID_QUIZ_EMOJIS:
        message_id, question_id, user_id = parse_values(react, user, guildid)

    if user_quiz_responses.already_answered(message_id, question_id, user_id):
        await react.remove(user)
        return

    user_quiz_responses.add_response(message_id, question_id, user_id)

    await react.remove(user)


async def parse_values(react, user, client, guildid):
    message_id = react.message.id
    question_id = react.message.embeds[0].footer.text
    quiz_id, quiz_question_number = question_id.split("_")
    user_answer = EMOJI_TO_ANSWER[react.emoji]

    user_id = str(user.id)
    members = get_members(react, client, guildid)

    return message_id, question_id, user_id


def get_members(client, reaction, guildid):
    guild = client.get_guild(guildid) or reaction.message.guild
    if guild is None:
        raise Exception(
            f"Warning: Unable to find a guild with the ID {guildid}")


async def dm_user(user, user_id, quiz_id, question_number, user_answer, members):
    question_dict = question_dict_mapping[quiz_id]
    question = question_dict[question_number]
    correct_answer = question["correctanswer"].lower()
    if user_answer == "show_answer":
        if "reasoning" in question:
            await user.send(f"The correct answer is '{correct_answer}'\n\n**Reasoning**: {question['reasoning']}")
            return
        else:
            await user.send(f"The correct answer is '{correct_answer}'")
        return

    answered_correctly = user_answer.lower() == correct_answer.lower()
    user_scores.handle_quiz_answer(user_id, quiz_id, answered_correctly)

    if answered_correctly:
        response_str = get_correct_answer_response_str(
            user_answer, question, "reasoning" in question)
    else:
        response_str = get_incorrect_answer_response_str(
            user_answer, correct_answer, question, "reasoning" in question)

    await user.send(response_str)
    return


def get_correct_answer_response_str(user_answer, question, with_reasoning):
    if with_reasoning:
        return f"🎉 Congratulations, your answer '{user_answer}' is correct!\n\n**Reasoning**: {question['reasoning']}"
    else:
        return f"🎉 Congratulations, your answer '{user_answer}' is correct!"


def get_incorrect_answer_response_str(user_answer, correct_answer, question, with_reasoning):
    if with_reasoning:
        return f"🤔 Your answer '{user_answer}' is incorrect. The correct answer is '{correct_answer}'.\n\n**Reasoning**: {question['reasoning']}"
    else:
        return f"🤔 Your answer '{user_answer}' is incorrect. The correct answer is '{correct_answer}'."
