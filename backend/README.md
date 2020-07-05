# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With the project dependencies installed, create a db for the project using command `dropdb trivia` and `createdb trivia` in the terminal. Update the [`config.py`](./config.py) file . Then run a flask db upgrade in the terminal to setup the tables and constraints
```bash
flask db upgrade
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Endpoints
### GET /categories
- General:
    - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
    - Request Arguments: None
    - Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
- Sample: `curl http://127.0.0.1:5000/categories`
- Response:
    ```
    {'1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"}

    ```
### GET /questions
- General:
    - Returns a list of question objects, categories objects, 
    current category and total number of questions in the database
    - Request Arguments: None
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
    - This endpoint is used to populate the home page route
- Sample: `curl http://127.0.0.1:5000/questions`
- Response:
    ```
    {
    "categories": {
        "1": "Science",
        "2": "History",
        "3": "Entertainment",
        "4": "Sports",
        "5": "Geography",
        "6": "Art"
    },
    "current_category": 1,
    "questions": [
        {
        "answer": "H2O",
        "category": 1,
        "difficulty": 3,
        "id": 36,
        "question": "Chemical formular for Water"
        },
        {
        "answer": "emc2",
        "category": 1,
        "difficulty": 3,
        "id": 38,
        "question": "Speed of light"
        },
        {
        "answer": "Blue",
        "category": 1,
        "difficulty": 3,
        "id": 39,
        "question": "What is considered the rarist form of color blindness?"
        },
        {
        "answer": "Rhopalocera",
        "category": 1,
        "difficulty": 3,
        "id": 40,
        "question": "What is the scientific name of a butterfly?"
        },...
    ],
    "success": true,
    "total_questions": 15
    }
    ```
### GET /categories/{id}/questions
- General:
    - Returns a list of question objects within a category, 
    current category and total number of questions in that category
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
    - This endpoint is used to populate the home page route
- Sample: `curl http://127.0.0.1:5000/categories/4/questions`
- Response:
    ```
    {
    "current_category": 4,
    "questions": [
        {
        "answer": "False",
        "category": 4,
        "difficulty": 1,
        "id": 52,
        "question": "Manchester United won the 2013-14 English Premier League."
        },...],
    "success": true,
    "total_questions": 6
    }
    ```
### POST /questions
- General:
    - This endpoint does two tasks: 
        - Search for a question
        - Create a new question 
    - Search: 
        - Searches for a question provided a searchterm is submitted
        - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
        - Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"organ"}'`
        - Request Arguments: `{"searchTerm":"organ"}`
        - Response: 
            ```
            {
            "questions": [
                {
                "answer": "Skin",
                "category": 1,
                "difficulty": 3,
                "id": 61,
                "question": "Which organ is responsible for touch and feelings"
                }
            ],
            "success": true,
            "total_questions": 1
            }
            ```
    - Create: 
        - Creates a new question using the submitted question, answer, category and difficulty. Returns the id of the created question, success value, total questions, and question list based on current page number to update the frontend. 
        - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
        - Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Which organ is responsible for touch and feelings", "answer":"Skin","category": "1", "difficulty":"3"}'`
        - Request Arguments: `{"question":"Which organ is responsible for touch and feelings", "answer":"Skin","category": "1", "difficulty":"3"}`
        - Response:
            ```
            {
            "categories": [1, 2, 3, 4, 5, 6],
            "created": 61,
            "current_category": 1,
            "questions": [
                {
                "answer": "H2O",
                "category": 1,
                "difficulty": 3,
                "id": 36,
                "question": "Chemical formular for Water"
                },...
            ],
            "success": true,
            "total_questions": 17
            }
            ```
### DELETE /questions/{id}
- General:
    - Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value, total questions, and question list based on current page number to update the frontend. 
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/16`
- Response:
    ```
    {
    "categories": [1, 2, 3, 4, 5, 6],
    "current_category": 1,
    "id": 45,
    "questions": [
        {
        "answer": "H2O",
        "category": 1,
        "difficulty": 3,
        "id": 36,
        "question": "Chemical formular for Water"
        },
        {
        "answer": "emc2",
        "category": 1,
        "difficulty": 3,
        "id": 38,
        "question": "Speed of light"
        },...
    ],
    "success": true,
    "total_questions": 16
    }
    ```
### POST /quizzes
- General: 
    - This endpoint fetches questions to play the quiz using the
    submitted category and previous question parameters 
    and return a random question within the given category, 
    if provided, and that is not one of the previous questions.
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"id": 1, "type": "Science"}, "previous_question": [1,4]}'`
- Request Arguments: `{"quiz_category":{"id": 1, "type": "Science"}, "previous_question": [1,4]}'`
- Response:
    ```
    {
    "previous_questions": [
        4, 1, 44 
    ],
    "question": {
        "answer": "Iron",
        "category": 1,
        "difficulty": 2,
        "id": 44,
        "question": "The element involved in making human blood red is which of the following?"
    },
    "success": true
    }
```

```
## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```