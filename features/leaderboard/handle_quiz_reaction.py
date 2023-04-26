import base64
import json

from discord import Client, Embed
from bot import commands
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

user_responses = {}  # Format: {message_id: {question_id: {user_id: answer}}}
user_scores = {}     # Format: {user_id: {quiz_id: {correct: int, incorrect: int }}}

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
        await send_user_dm(react, user, question_id)


async def send_user_dm(react, user, question_id):
    quiz_id, question_number = question_id.split("_")
    question_number = int(question_number)
    user_answer = EMOJI_TO_ANSWER[react.emoji]

    response_str = create_response_str(
        quiz_id, question_number, user_answer)

    await user.send(response_str)


def is_valid_quiz_emoji(emoji):
    return emoji in VALID_QUIZ_EMOJIS


def user_already_reacted(user_id, msg_id, question_id):
    return msg_id in user_responses and question_id in user_responses[msg_id] and user_id in user_responses[msg_id][question_id]


def add_user_response(msg_id, question_id, user_id, user_answer):
    global user_responses

    if msg_id not in user_responses:
        user_responses[msg_id] = {}
    if question_id not in user_responses[msg_id]:
        user_responses[msg_id][question_id] = {}
        user_responses[msg_id][question_id][user_id] = user_answer


def create_response_str(user_id, quiz_id, question_number, user_answer):
    global user_scores

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

# ------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------- leaderboard update logic below -------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------

# only load scores from leaderboard if we have not done so already
loaded_scores_from_leaderboard = False


async def handle_update_leaderboard(client: Client, guildid: str, leaderboardid: str):
    global user_scores
    global loaded_scores_from_leaderboard

    leaderboard_channel, member_dict = await load_channel_and_members(client, guildid, leaderboardid)

    if not user_scores and not loaded_scores_from_leaderboard:
        user_scores = await load_user_scores_from_existing_leaderboard(
            leaderboard_channel, client)
        loaded_scores_from_leaderboard = True

    leaderboard_embed = await create_leaderboard_embed(member_dict)
    await upsert_leaderboard_message(leaderboard_embed, leaderboard_channel, client)


async def load_channel_and_members(client, guildid, leaderboardid):
    await client.wait_until_ready()
    if guildid is None or leaderboardid is None:
        print(f"missing required guild or leaderboard channel id")
        return
    guild = client.get_guild(int(guildid))
    member_dict = {str(member.id): member for member in guild.members}
    leaderboard_channel = guild.get_channel(int(leaderboardid))
    return leaderboard_channel, member_dict


async def create_leaderboard_embed(member_dict):
    global user_scores

    leaderboard_embed = Embed(
        title="Quiz Commands Leaderboard", color=0x006400)

    # leaderboard embed: overall
    sorted_overall_user_scores = sort_overall_user_scores()
    overall_leaderboard_str = create_overall_leaderboard_str(
        sorted_overall_user_scores, member_dict)
    leaderboard_embed.add_field(
        name="Overall", value=overall_leaderboard_str, inline=False)

    # leaderboard embed: each quiz leaderboard
    user_scores_by_quiz = create_user_scores_by_quiz_data()
    for prefix, scores in user_scores_by_quiz.items():
        sorted_users_by_quiz = sorted(scores.items(), key=lambda x: (
            x[1]["correct"], x[1]["incorrect"]), reverse=True)
        prefix_leaderboard_desc = create_quiz_leaderboard_str(
            sorted_users_by_quiz, member_dict)
        leaderboard_embed.add_field(
            name=prefix.upper(), value=prefix_leaderboard_desc, inline=False)

    # leaderboard embed: base64 encoded user_scores
    user_scores_json = json.dumps(user_scores)
    user_scores_base64 = base64.b64encode(user_scores_json.encode()).decode()
    leaderboard_embed.add_field(
        name="Parity", value=f"```{user_scores_base64}```", inline=False)

    # leaderboard embed: footer
    leaderboard_embed.set_footer(
        text="Note: The leaderboard is updated once per hour. \n To learn more about the quiz commands, run `/commands` in #bot-commands")

    return leaderboard_embed


def sort_overall_user_scores():
    global user_scores

    overall_scores = {}
    for user_id, scores in user_scores.items():
        overall_correct = sum([s["correct"] for s in scores.values()])
        overall_incorrect = sum([s["incorrect"] for s in scores.values()])
        overall_scores[user_id] = {
            "correct": overall_correct,
            "incorrect": overall_incorrect
        }

    sorted_user_scores = sorted(overall_scores.items(), key=lambda x: (
        x[1]["correct"], x[1]["incorrect"]), reverse=True)

    return sorted_user_scores


def create_overall_leaderboard_str(sorted_user_scores, member_dict):
    overall_leaderboard_desc = ""
    rank = 1
    for user_id, scores in sorted_user_scores:
        member = member_dict.get(user_id)
        if member is not None:
            username = member.display_name
        else:
            username = f"Unknown User ({user_id})"
        correct = scores["correct"]
        incorrect = scores["incorrect"]
        overall_leaderboard_desc += f"{rank}. **{username}**: {correct} correct, {incorrect} incorrect\n"
        rank += 1
        if rank > 5:
            break
    return overall_leaderboard_desc


def create_user_scores_by_quiz_data():
    global user_scores

    user_scores_by_quiz_data = {p: {} for p in QUESTION_DICT_MAPPING}
    for user_id, scores in user_scores.items():
        for prefix, score in scores.items():
            user_scores_by_quiz_data[prefix][user_id] = {
                "correct": score["correct"], "incorrect": score["incorrect"]}
    return user_scores_by_quiz_data


def create_quiz_leaderboard_str(sorted_users_by_quiz, member_dict):
    prefix_leaderboard_desc = ""
    rank = 1
    for user_id, user_scores_for_quiz in sorted_users_by_quiz:
        member = member_dict.get(user_id)
        if member is not None:
            username = member.display_name
        else:
            username = f"Unknown User ({user_id})"
        correct = user_scores_for_quiz["correct"]
        incorrect = user_scores_for_quiz["incorrect"]
        prefix_leaderboard_desc += f"{rank}. **{username}**: {correct} correct, {incorrect} incorrect\n"
        rank += 1
        if rank > 5:
            break
    return prefix_leaderboard_desc


def create_quiz_leaderboard_str(sorted_users_by_quiz, member_dict):
    prefix_leaderboard_desc = ""
    rank = 1
    for user_id, user_scores_for_quiz in sorted_users_by_quiz:
        member = member_dict.get(user_id)
        if member is not None:
            username = member.display_name
        else:
            username = f"Unknown User ({user_id})"
        correct = user_scores_for_quiz["correct"]
        incorrect = user_scores_for_quiz["incorrect"]
        prefix_leaderboard_desc += f"{rank}. **{username}**: {correct} correct, {incorrect} incorrect\n"
        rank += 1
        if rank > 5:
            break
    return prefix_leaderboard_desc


async def load_user_scores_from_existing_leaderboard(leaderboard_channel, client):
    user_scores = {}  # default
    leaderboard_message = None
    async for message in leaderboard_channel.history():
        if message.author == client.user:
            leaderboard_message = message
            break
    user_scores_base64 = get_encoded_user_scores_from_embeds(
        leaderboard_message)
    try:
        user_scores_json = base64.b64decode(
            user_scores_base64.encode()).decode()
        user_scores = json.loads(user_scores_json)
    except Exception as e:
        print(
            f"Error decoding base64 user_scores: {e}")
    return user_scores


def get_encoded_user_scores_from_embeds(leaderboard_message):
    if leaderboard_message is not None:
        for embed in leaderboard_message.embeds:
            for field in embed.fields:
                if field.name == "Parity":
                    return field.value.strip('```')


async def upsert_leaderboard_message(leaderboard_embed, leaderboard_channel, client):
    leaderboard_message = None
    async for message in leaderboard_channel.history():
        if message.author == client.user:
            leaderboard_message = message
            break
    if leaderboard_message is None:
        leaderboard_message = await leaderboard_channel.send(embed=leaderboard_embed)
    else:
        await leaderboard_message.edit(embed=leaderboard_embed)
