import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# setup paginated questions


def paginate_questios(request, selections):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selections]
    current_questions = questions[start: end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Set up CORS. Allow '*' for origins
    cors = CORS(app, resources={"/": {"origins": "*"}})

    # Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers",
                             "Content-Type, Authorization, true")
        response.headers.add("Access-Control-Allow-Methods",
                             "GET, PUT, POST, DELETE, OPTIONS")
        return response

    """
  Handle GET requests for all available categories
  """
    @app.route("/categories")
    def retrieve_categories():

        # get all categories and add to dict
        categories = Category.query.order_by(Category.id).all()
        categories_dict = {
            category.id: category.type for category in categories}

        # abort 404 if no categories found
        if len(categories_dict) == 0:
            abort(404)

        # return json to the client
        return jsonify({
            "success": True,
            "categories": categories_dict
        })

    """
  Handle GET requests for all paginated questions
  """
    @app.route("/questions")
    def retrieve_questions():

        # get all questions
        selections = Question.query.order_by(Question.id).all()
        current_questions = paginate_questios(request, selections)

        # get all categories and add to dict
        categories = Category.query.order_by(Category.id).all()
        categories_dict = {
            category.id: category.type for category in categories}

        # abort 404 if no questions found
        if len(current_questions) == 0:
            abort(404)

        # return a list of questions, number of total questions
        # current category, categories.
        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": len(selections),
            "categories": categories_dict
        })

    """
  Handle DELETE requests for deleting a question by given id
  """
    @app.route("/questions/<int:id>", methods=["DELETE"])
    def delete_question(id):

        try:
            # find the question by a given id
            question = Question.query.filter(Question.id == id).one_or_none()

            # abort 404 if no question found
            if question is None:
                abort(404)

            # delete the question in db
            question.delete()

            # return json file
            return jsonify({
                "success": True,
                "deleted": question.id
            })

        except:
            # abort 422 if unprocessable
            abort(422)

    """
  Handle POST requests for creating a new question and searching user input
  """
    @app.route("/questions", methods=["POST"])
    def create_question():

        # retrieve the new data from user input
        body = request.get_json()

        # get the user search term from request body
        search_term = body.get("searchTerm", None)

        # If there is no search term,
        # we simple add new question to the db from form input
        if search_term is None:

            # retrieve new data from request body
            new_question = body.get("question", None)
            new_answer = body.get("answer", None)
            new_category = body.get("category", None)
            new_difficulty = body.get("difficulty", None)

            # abort 422 if any of fields are blank
            if ((new_question is None) or (new_answer is None)
                    or (new_category is None) or (new_difficulty is None)):
                abort(422)

            try:
                # create new question
                question = Question(question=new_question, answer=new_answer,
                                    category=new_category, difficulty=new_difficulty)

                # add new data into db
                question.insert()

                # get updated data
                selections = Question.query.order_by(Question.id).all()
                current_questions = paginate_questios(request, selections)

                # return json to client
                return jsonify({
                    "success": True,
                    "created": question.id,
                    "questions": current_questions,
                    "total_questions": len(selections)
                })

            except:
                # abort 422 if unprocessable
                abort(422)

        # if we do have search term
        else:
            # get all data based on the search term
            selections = Question.query.filter(
                Question.question.ilike(f"%{search_term}%")).all()

            # abort 404 if no questions found based on search term
            if len(selections) == 0:
                abort(404)

            # paginate the results
            current_questions = paginate_questios(request, selections)

            # return json to client
            return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": len(Question.query.all())
            })

    """
  Handle GET requests to get questions based on category
  """
    @app.route("/categories/<int:id>/questions")
    def get_questions_by_category(id):

        # get the category based on the id
        category = Category.query.filter(Category.id == id).one_or_none()

        # abort 404 if no category found
        if category is None:
            abort(404)

        # retrieve all questions based on the category id
        selections = Question.query.filter(
            Question.category == str(category.id)).all()

        current_questions = paginate_questios(request, selections)

        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": len(Question.query.all()),
            "current_category": category.type
        })

    """
  Handle POST requests to get questions to play the quiz
  """
    @app.route("/quizzes", methods=["POST"])
    def play_quizzes():

        # get the data from user input
        body = request.get_json()

        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)
        quiz_category_id = quiz_category['id']

        # retrieve nexr question not in previous questions
        if quiz_category_id == 0:
            next_question = Question.query.filter(
                Question.id.notin_(previous_questions)).first()
        else:
            next_question = Question.query.filter(Question.id.notin_(
                previous_questions)).filter_by(category=quiz_category_id).first()

        # abort 404 there is no question
        if next_question is None:
            abort(404)

        # return json to the client
        return jsonify({
            'success': True,
            'question': next_question.format()
        })

    '''
  Error handlers for all expected errors including 404, 422 and 400. 
  '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 404

    return app
