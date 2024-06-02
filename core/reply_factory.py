
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if current_question_id is None:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    # session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    """
    Validates and stores the answer for the current question to django session.
    """
    if "responses" in session:
        session["responses"][current_question_id] = answer
    else:
        session["responses"] = {current_question_id: answer}
    if current_question_id is None:
        expected_answer = BOT_WELCOME_MESSAGE
    else:
        expected_answer = PYTHON_QUESTION_LIST[current_question_id]["answer"]
    is_answer_correct = answer == expected_answer
    if is_answer_correct:
        bot_response = "Correct"
    else:
        bot_response = "Incorrect"
    return is_answer_correct, bot_response


def get_next_question(current_question_id):
    """
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    """
    if current_question_id is None:
        next_question_id = 0
    else:
        next_question_id = current_question_id + 1
    if next_question_id < len(PYTHON_QUESTION_LIST):
        return PYTHON_QUESTION_LIST[next_question_id]["question_text"], next_question_id
    return "", -1


def generate_final_response(session):
    """
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    """
    responses = session.get("responses")
    score = 0
    max_score = len(PYTHON_QUESTION_LIST)
    if responses:
        for question_id, answer in responses.items():
            if PYTHON_QUESTION_LIST[question_id]["answer"] == answer:
                score += 1
    return f"Score: {score} out of {max_score}"
