import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.app.config.from_object('config')
        setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            "question": "What is your other name",
            "answer": "Chinedu",
            "category": 2,
            "difficulty": 3
            }

        self.data1_missing_question = {
            "question": "",
            "answer": "Chinedu",
            "category": 2,
            "difficulty": 3
            }

        self.data2_missing_answer = {
            "question": "Full meaning of WHO",
            "answer": "",
            "category": 2,
            "difficulty": 3
            }

        self.data3_missing_category = {
            "question": "Full meaning of WHO",
            "answer": "World Health Organization",
            "category": "",
            "difficulty": 3
            }

        self.data4_missing_difficulty = {
            "question": "Full meaning of WHO",
            "answer": "World Health Organization",
            "category": 2,
            "difficulty": ""
            }

        self.new_searchterm = {
            "searchTerm": "Water"
            }

        self.random_quizzes={
            "quiz_category": {"id": 0, "type": ""},
            "previous_questions": []
            }

        self.new_quizzes={
            "quiz_category": {"id": 1, "type": "Science"},
            "previous_questions": []
            }

        self.no_previous_question_quizzes={
            "quiz_category": {"id": 1, "type": "Science"}
            }

        self.no_id_quizzes={
            "quiz_category": {"id": "", "type": ""},
            "previous_questions": []
            }
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # /categories
    def test_categories_route(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']))

    def test_404_resource_not_found_on_categories(self):
        res = self.client().get('/categories/300')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_405_method_not_allowed_on_categories_route(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # /questions
    def test_get_paginated_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    def test_405_method_not_allowed_on_questions_route(self):
        res = self.client().get('/questions/3')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')
    
    def test_delete_question(self):
        res = self.client().delete('/questions/14')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 14)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_if_question_does_not_exit(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        
    def test_create_new_questions(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_400_no_question_create_new_questions(self):
        res = self.client().post('/questions', json=self.data1_missing_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_400_no_answer_create_new_questions(self):
        res = self.client().post('/questions', json=self.data2_missing_answer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_400_no_category_create_new_questions(self):
        res = self.client().post('/questions', json=self.data3_missing_category)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_400_no_difficulty_create_new_questions(self):
        res = self.client().post('/questions', json=self.data4_missing_difficulty)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_405_for_question_creation_not_allowed(self):
        res = self.client().post('/questions/45')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_200_search_for_questions(self):
        res = self.client().post('/questions', json=self.new_searchterm)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_405_wrong_methods_on_questions(self):
        res = self.client().patch('/questions/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # /categories/<id>/questions
    def test_retrieve_all_questions_within_a_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['current_category'])

    def test_404_no_category_not_present(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        
    def test_405_wrong_methods_on_category_id_question(self):
        res = self.client().post('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # /quizzes
    def test_200_random_quizzes(self):
        res = self.client().post('/quizzes', json=self.random_quizzes)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(type(data['previous_questions']), list)
        self.assertEqual(type(data['question']), dict)
        self.assertTrue(len(data['previous_questions']))

    def test_200_selected_quizzes_by_category(self):
        res = self.client().post('/quizzes', json=self.new_quizzes)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(type(data['previous_questions']), list)
        self.assertEqual(type(data['question']), dict)
        self.assertTrue(len(data['previous_questions']))

    def test_404_no_id_quizzes(self):
        res = self.client().post('/quizzes', json=self.no_id_quizzes)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_404_no_previous_questions_quizzes(self):
        res = self.client().post('/quizzes', json=self.no_previous_question_quizzes)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_405_method_not_allowed_quizzes(self):
        res = self.client().get('/quizzes', json=self.new_quizzes)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()