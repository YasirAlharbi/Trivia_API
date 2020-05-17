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
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}@{}/{}".format("akira", 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # get categories should return success response
    def test_200_get_categories(self):
        res = self.client().get('/categories')
        
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_get_paginated_questions(self):
        """Tests question pagination success"""

        # get response and load data
        response = self.client().get('/questions')
        data = json.loads(response.data)

        # check status code and message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

        # check that total_questions and questions return data
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['questions']))

    def test_404_request_beyond_valid_page(self):
        """Tests question pagination failure 404"""

        # send request with bad page data, load response
        response = self.client().get('/questions?page=100')
        data = json.loads(response.data)

        # check status code and message
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # delete existing question should return success response
    def test_200_delete_existing_question(self):
        res = self.client().delete('/questions/12')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEquals(data['success'], True)

    
    # delete non existing question should return 404 response
    def test_404_delete_non_existing_question(self):
        res = self.client().delete('/questions/999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")
    
        # post non existing question should return success response
    def test_200_post_non_existing_question(self):
        res = self.client().post('/questions', json={'question':"question non existing", 
        'answer': "non existing answer", 'difficulty': 3, 'category': "3"})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    # post question using wrong parameter (category non existing) should return 422 response
    def test_422_post_question_with_bad_parameters(self):
        res = self.client().post('/questions', json={'question':"question non existing", 
        'answer': "non existing answer", 'difficulty': 10, 'category': "10"})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")
    
     # get questions using existing search term should return success response
    def test_200_get_question_by_search_term(self):
        res = self.client().post('/questions', json={'searchTerm':"the"})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    # get questions using non existing search term should return 404 response
    def test_404_get_question_by_inexisten_search_term(self):
        res = self.client().post('/search', json={'searchTerm':"supercalifragilistico"})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], "Resource Not Found")

    
    # get questions by existing category should return success response
    def test_200_get_questions_by_category(self):
        res = self.client().get('/categories/5/questions')
        
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    # get questions by non existing category should return 404 response
    def test_404_get_questions_by_inexistent_category(self):
        res = self.client().get('/categories/99/questions')
        
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], "Resource Not Found")


    # get quiz questions using correct request body should return success response
    def test_200_get_quizzes(self):
        res = self.client().post('/quizzes', json={'previous_questions':[], 'quiz_category': {'id':1,'type':'Science'}})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    # get quiz questions using wrong request parameters should return 404 response
    def test_404_get_quizzes_of_inexistent_category(self):
        res = self.client().post('/quizzes', json={'previous_questions':[], 'quiz_category': {'id':99,'type':'Non existing'}})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], "Resource Not Found")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()