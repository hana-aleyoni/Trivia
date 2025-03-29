import os
from flask import Flask, make_response, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.id).all()

        if categories is None:
            abort(404)

        formatted_categories = {category.id: category.type for category in categories}

        return jsonify({
            'success': True,
            'categories': formatted_categories,
            'total_categories':len(Category.query.all())
        })


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = Question.query.all()
        total_questions = len(questions)
        current_questions = questions[start:end]

        if current_questions is None:
            abort(404)


        formatted_questions = [question.format() for question in current_questions]
        categories = Category.query.all()
        formatted_categories = {category.id: category.type for category in categories}
        if len(formatted_questions) == 0:
         abort(404, description="Resource not found")

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': total_questions,
            'categories': formatted_categories
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            

            if question is None:
                abort(404, description=f"Question with id {question_id} not found")

            question.delete()
            remaining_questions = Question.query.all()
            total_questions = len(remaining_questions)
            return jsonify({
                'success': True,
                'deleted': question_id,
                'total_questions': total_questions
            })

        except Exception as e:
            print(e)
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def add_question():
        try:
            body = request.get_json()

            question = body.get('question', None)
            answer = body.get('answer', None)
            category = body.get('category', None)
            difficulty = body.get('difficulty', None)
            if not (question and answer and category and difficulty):
             abort(422, description='One or more required fields are missing or empty.')
            if isinstance(category, str):
             category = int(category) 

            category_obj = Category.query.filter_by(id=category).first()
            if not category_obj:
             abort(422) 

            new_question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
            new_question.insert()
            total_questions = len(Question.query.all())
            questions = Question.query.all()
            formatted_questions = [question.format() for question in questions]

            return jsonify({
                'success': True,
                'created': new_question.id,
                'total_questions': total_questions,
                'questions': len(formatted_questions)
            }),200

        except Exception as e:
            print(e)
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', None)

        if not search_term:
            abort(422)

        search_term = body.get('searchTerm', None)
        try:
            search_results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            formatted_questions = [question.format() for question in search_results]
            if len(formatted_questions) == 0:
             return jsonify({
                'success': True,
                'questions': [],
                'total_questions': 0
            }), 200

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(formatted_questions)
            }),200

        except Exception as e:
            print(e)
            abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        try:
            category = Category.query.filter_by(id=category_id).first()

            if not category:
             abort(404, description="Category not found")
             
            questions = Question.query.filter(Question.category == str(category_id)).all()
            formatted_questions = [question.format() for question in questions]

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(formatted_questions),
                'current_category': category_id
            })

        except Exception as e:
            print(e)
            abort(404)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            body = request.get_json()

            previous_questions = body.get('previous_questions', [])
            quiz_category = body.get('quiz_category', None)

            if quiz_category is None:
                abort(422)

            category_id = int(quiz_category['id'])

            if category_id == 0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter(Question.category == str(category_id)).all()

            remaining_questions = [question.format() for question in questions if question.id not in previous_questions]

            if len(remaining_questions) > 0:
                selected_question = random.choice(remaining_questions)
            else:
                selected_question = None

            return jsonify({
                'success': True,
                'question': selected_question
            })

        except Exception as e:
            print(e)
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable'
        }), 422

    return app

