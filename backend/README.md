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
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
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

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET '/questions'
POST '/questions'
DELETE '/questions'
POST '/questions/search'
GET '/categories/<int:id>/questions'
POST '/quizzes'

GET '/categories'
- Fetches a list of categories , the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories,  pairs. 
- status code: 200

{
    'categories': [
        art,
        science,
        ...
    ],
    'success': True
}

GET '/questions'
- Fetches a list of questions
- Pagination : 10
- Request Arguments: None
- Returns: An object with: 
    - list of questions
    - Total number of questions
    - list of categories
    - current category
- status code : 200

{
  "categories": [
    "Science",
    ...
  ],
  "current_category": "all",
  "questions": [
    {
      "answer": "Genesis",
      "category": "Art",
      "category_id": 3,
      "difficulty": 2,
      "id": 12,
      "question": "what is the first book in the bible"
    },
    ...
  ],
  "success": true,
  "total_questions": 23
}

POST '/questions'
- Creates a new question
- Request Arguments: None
- Returns: An object with a message 
- status code : 201  

- sample post data : 
{
	"question": "question",
	"answer": "answer",
	"category": 1,
	"difficulty": 1
}

returned data:
{
    'success': True,
    'message': 'Question Successfully added.'
}

DELETE '/questions'
- Deletes a particular question.
- Request Arguments: None
- Returns: An object with a messsage. 
- status code on succes: 200
- status code on failure: 404

returned data:
{
    'success': True,
    'message': 'Question Successfully deleted.'
}

POST '/questions/search'
- Fetches questions that have th e search term
- Request Arguments: None
- Returns: An object with: 
    - list of questions
    - Total number of questions
    - list of categories
    - current category
- status code: 200

- sample post data : 
{
	"searchTerm": "happy"
}


POST '/quizzes'
- Fetches a list of questions based on selected category in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with 2 keys,
  - success that contains a boolean that indicates success/failure of the request.
  - question that contains a question to display next.
- status code: 200

{
  "question": {
    "answer": "...",
    "category": 1,
    "difficulty": 1,
    "id": 1,
    "question": "..."
  },
  "success": true
} 

GET '/categories/<int:id>/questions'
- Fetches questions based on selected category
- Request Arguments: None
- Returns: An object with: 
    - list of questions
    - Total number of questions
    - list of categories
    - current category
- status code: 200


Status Codes
201 - created
200 - ok
404 - Not found
400 - Bad request
422 - Unprocessable

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
