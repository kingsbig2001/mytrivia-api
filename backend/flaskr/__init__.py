import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random
from models import setup_db, Question, Category

#maximum amount of questions per page to be returned
QUESTIONS_PER_PAGE = 10

#Pagination for Questions
def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

#Initialising flask app
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/questions/*": {"origins": "*"}, r"/categories/*": {"origins": "*"}, r"/quizzes/*": {"origins": "*"}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    """Get all categories formatted as {1: 'Science', 2: 'Geography', ...} """
    categories = Category.query.order_by(Category.id).all()
    categories_formatted = {}
    for category in categories:
      categories_formatted[category.id] = category.type
    
    return jsonify({
        "success": True,
        "categories": categories_formatted
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def retrieve_all_questions():
    """Get all categories formatted as {1: 'Science', 2: 'Geography', ...} """
    categories = Category.query.order_by(Category.id).all()
    categories_formatted = {}

    for category in categories:
      categories_formatted[category.id] = category.type
    #Get list of categories ids
    current_category = list(categories_formatted)[0]

    #Paginate questions
    selection = Question.query.filter(Question.category == current_category).order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)
    
    return jsonify({
      "success" : True,
      "questions": current_questions,
      "total_questions" : len(selection),
      "categories" : categories_formatted,
      "current_category" : current_category
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def remove_a_question(id):
    #fetch the question object
    question = Question.query.filter(Question.id == id).one_or_none()

    try:
      if question is None:
        abort(404)

      question.delete()

      #update the view with the correct questions after deleting
      categories = Category.query.order_by(Category.id).all()
      categories_ids = [category.id for category in categories ]
      current_category = question.category

      #paginate the list of questions
      selection = Question.query.filter(Question.category == current_category).order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
        "success" : True,
        "id" : question.id,
        "questions" : current_questions,
        "total_questions" : len(selection),
        "categories": categories_ids,
        "current_category": current_category
      })
      
    except:
      abort(404)
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  '''
  This endpoint handles a POST request to add a question
  as well as search for a question
  '''
  @app.route('/questions', methods=['POST'])
  def add_a_question():
    #Gets data from the client
    body = request.get_json()

    #retrieves search term from the frontend
    search_term = body.get('searchTerm')

    '''
    Checks for searchterm to ascertain what user is doing.
    a valid searchterm indicates a POST request for Searching question
    in the database
    '''
    if search_term:
      search_term_formatted = "%{}%".format(search_term)

      #Query the database using the searhterm_formatted
      questions = Question.query.filter(Question.question.ilike(search_term_formatted)).all()
      current_questions = paginate_questions(request, questions)

      return jsonify({
        "success" : True,
        "questions": current_questions,
        "total_questions": len(questions)
      })
    #In the absence of a searchterm, continue with 
    # adding a question to the db
    else:
      new_question = body.get('question')
      new_answer = body.get('answer')
      new_category = body.get('category')
      new_difficulty = body.get('difficulty')

      #lookup db to ensure no duplicate question
      check_question = Question.query.filter(Question.question == new_question).filter(Question.category == new_category).one_or_none()

      if check_question is None:
        try:
          question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)

          question.insert()

          #update the frontend after adding a question successfully
          current_category = question.category
          categories = Category.query.order_by(Category.id).all()
          categories_ids = [category.id for category in categories ]

          #paginate list of questions
          selection = Question.query.filter(Question.category == current_category).order_by(Question.id).all()
          current_questions = paginate_questions(request, selection)

          return jsonify({
            "success" : True,
            "questions": current_questions,
            "total_questions" : len(selection),
            "categories" : categories_ids,
            "current_category" : current_category,
            "created" : question.id
          }),201
      
        except:
          abort(422)
      else:
        abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions')
  def retrieve_questions_categories(id):
    #fetch list of questions in a specified category(id)
    # and paginate the result
    selection = Question.query.filter(Question.category == id).order_by(Question.id).all()
    questions = paginate_questions(request, selection)

    return jsonify({
      "success" : True,
      "questions": questions,
      "total_questions" : len(selection),
      "current_category": id
    })


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def trivia_quiz():
    body = request.get_json()

    previous_questions = body.get('previous_questions')
    quiz_category = body.get('quiz_category')

    #Select all questions in the database
    if quiz_category['id'] == 0:
      questions = Question.query.filter(~Question.id.in_(previous_questions)).all()
      
    #Select questions within a specified category(quiz_category)
    else:
      questions = Question.query.filter(Question.category == quiz_category['id']).filter(~Question.id.in_(previous_questions)).all()
    
    # randomize the questions
    random.shuffle(questions)

    #return first question of the reshuffled list of questions
    current_question = questions[0].format()
    #update the list of previous questions
    previous_questions.append(current_question['id'])
    
    return jsonify({
      "success" : True,
      "question" : current_question,
      "previous_questions": previous_questions
    })  

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success" : False,
      "message" : "resource not found",
      "error" : 404
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success" : False,
      "message" : "unprocessable",
      "error" : 422
    }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success" : False,
      "message" : "bad request",
      "error" : 400
    }), 400

  @app.errorhandler(405)
  def not_allowed(error):
    return jsonify({
      "success" : False,
      "message" : "method not allowed",
      "error" : 405
    }), 405
  return app

    