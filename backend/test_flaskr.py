import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category ,engine, SessionLocal, Base
from settings import DB_NAME, DB_USER, DB_PASSWORD



class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        # self.database_name = "trivia_test"
        # self.database_path = 'postgresql://postgres@localhost:5432/trivia_test'
        
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@localhost:5432/{os.getenv("DB_NAME")}'
        })

        self.client = self.app.test_client
        self.database_name = os.getenv("DB_NAME")
        self.database_path = f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@localhost:5432/{self.database_name}'

        with self.app.app_context():
            Base.metadata.create_all(bind=engine)
            self.db = SessionLocal()


        self.new_question = {
            'question': 'What is the capital of France?',
            'answer': 'Paris',
            'category': 'Geography',
            'difficulty': 3
        }
        self.quiz_data = {
            'previous_questions': [],
            'quiz_category': {'type': 'Science', 'id': '1'}
        }
        self.search_data = {
            'searchTerm': 'question'
        }

    
    def tearDown(self):
        """Executed after reach test"""
        with self.app.app_context():
            self.db.close()
            Base.metadata.drop_all(bind=engine)
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    
    def test_get_categories(self):
       with self.app.app_context(): 
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'],True)
        self.assertTrue(len(data['categories']))

    def test_404_get_categories_failure(self):
       with self.app.app_context(): 
        res = self.client().get('/categories/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'],False)
        self.assertEqual(data['message'], 'Resource not found')



    
    def test_get_questions(self):
       with self.app.app_context(): 
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'],True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_404_get_questions_failure(self):
       with self.app.app_context(): 
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'],False)
        self.assertEqual(data['message'], 'Resource not found')  





    # ///
    def test_delete_question(self):
        with self.app.app_context(): 
         question_id_to_delete = 6
         res = self.client().delete(f'/questions/{question_id_to_delete}')
         data = json.loads(res.data)

         self.assertEqual(res.status_code, 200)
         self.assertTrue(data['success'])
         self.assertEqual(data['deleted'], question_id_to_delete)
         self.assertTrue(data['total_questions'])
    # ///
    def test_422_delete_question_not_exist(self):
       with self.app.app_context(): 
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'],False)
        self.assertEqual(data['message'], 'Unprocessable')  




    
    def test_create_question(self):
       with self.app.app_context(): 
        category = Category.query.filter_by(type=self.new_question['category']).first()
        category_id = category.id if category else None

        self.new_question['category'] = category_id

        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        if res.status_code == 200:
         self.assertTrue(data['success'],True)
         self.assertTrue(data['created'])
         self.assertTrue(len(data['questions']) > 0)
        else:
            self.assertEqual(res.status_code, 422) 


    def test_405_create_question_not_allowed(self):
       with self.app.app_context(): 
        res = self.client().post('/questions/22', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'],False)
        self.assertEqual(data['message'], 'Method not allowed')




    def test_search_questions(self):
       with self.app.app_context(): 
        res = self.client().post('/questions/search', json=self.search_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200) 
        self.assertTrue(data['success'])  
        self.assertTrue('questions' in data) 
        self.assertTrue('total_questions' in data) 
        if len(data['questions']) > 0:
            self.assertTrue(data['total_questions'] > 0) 
        else:
            self.assertEqual(data['total_questions'], 0)

    def test_search_questions_no_results(self):
       with self.app.app_context(): 
        res = self.client().post('/questions/search', json={'searchTerm': 'applejacks'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0)




    def test_get_questions_by_category(self):
       with self.app.app_context(): 
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], 3)

    def test_404_get_questions_by_category_failure(self):
       with self.app.app_context():
        res = self.client().get(f'/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)  
        self.assertFalse(data['success']) 
        self.assertEqual(data['message'], 'Resource not found') 





    def test_play_quiz(self):
       with self.app.app_context(): 
        res = self.client().post('/quizzes', json=self.quiz_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])

    def test_422_play_quiz_failure(self):
       with self.app.app_context(): 
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Unprocessable')
   


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()