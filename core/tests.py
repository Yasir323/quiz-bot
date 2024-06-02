from django.test import TestCase, RequestFactory
from unittest.mock import patch

from .reply_factory import generate_bot_responses, record_current_answer, get_next_question, generate_final_response
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


class BotResponseTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.session = {}

    def test_generate_bot_responses_initial(self):
        message = BOT_WELCOME_MESSAGE
        self.session["current_question_id"] = None
        self.session["responses"] = {}

        responses = generate_bot_responses(message, self.session)

        self.assertIn(BOT_WELCOME_MESSAGE, responses)
        self.assertEqual(self.session["current_question_id"], 0)

    def test_generate_bot_responses_correct_answer(self):
        self.session["current_question_id"] = 0
        message = PYTHON_QUESTION_LIST[0]["answer"]
        self.session["responses"] = {}

        responses = generate_bot_responses(message, self.session)

        self.assertIn(PYTHON_QUESTION_LIST[1]["question_text"], responses)
        self.assertEqual(self.session["current_question_id"], 1)

    def test_generate_bot_responses_incorrect_answer(self):
        self.session["current_question_id"] = 0
        message = "Wrong answer"
        self.session["responses"] = {}

        responses = generate_bot_responses(message, self.session)

        self.assertIn("Incorrect", responses)
        self.assertEqual(self.session["current_question_id"], 0)

    def test_record_current_answer_correct(self):
        answer = "Correct answer"
        current_question_id = 0
        self.session["responses"] = {}

        PYTHON_QUESTION_LIST[0] = {"question": "Q1", "answer": "Correct answer"}

        success, response = record_current_answer(answer, current_question_id, self.session)
        self.assertTrue(success)
        self.assertEqual(response, "Correct")

    def test_record_current_answer_incorrect(self):
        answer = "Wrong answer"
        current_question_id = 0
        self.session["responses"] = {}

        PYTHON_QUESTION_LIST[0] = {"question": "Q1", "answer": "Correct answer"}

        success, response = record_current_answer(answer, current_question_id, self.session)
        self.assertFalse(success)
        self.assertEqual(response, "Incorrect")

    def test_get_next_question(self):
        current_question_id = 0
        next_question, next_question_id = get_next_question(current_question_id)
        self.assertEqual(next_question, PYTHON_QUESTION_LIST[1]["question_text"])
        self.assertEqual(next_question_id, 1)

    def test_get_next_question_last(self):
        current_question_id = len(PYTHON_QUESTION_LIST) - 1
        next_question, next_question_id = get_next_question(current_question_id)
        self.assertEqual(next_question, "")
        self.assertEqual(next_question_id, -1)

    def test_generate_final_response(self):
        self.session["responses"] = {0: PYTHON_QUESTION_LIST[0]["answer"], 1: "Wrong answer"}

        final_response = generate_final_response(self.session)
        self.assertEqual(final_response, f"Score: 1 out of {len(PYTHON_QUESTION_LIST)}")
