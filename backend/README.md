# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Documentation Example

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Reference
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
  "error": 422,
  "message": "Unprocessable",
  "success": false
}
```
The API will return three error types when requests fail:
- 400: Bad request
- 404: Resource not found
- 405: Method not allowed
- 422: Unprocessable 

### Endpoints 
#### GET /categories
- Fetches a list of all categories available in the trivia database.
- Request Arguments: None
- Returns:
  - success: boolean indicating the success of the request.
  - categories: dictionary of categories where keys are category IDs and values are category types.
  - total_categories: total number of categories available.

- Sample: `curl http://127.0.0.1:5000/categories`

``` 
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_categories": 6
}

```

#### GET /questions
- Fetches a paginated list of trivia questions.
- Request Arguments: 
  - page (optional, default=1): Specifies the page number for pagination, starting from 1.
- Returns:
  - success: boolean indicating the success of the request.
  - questions: list of formatted question objects based on the specified page.
  - total_questions: total number of questions available in the database.
  - categories: dictionary of categories where keys are category IDs and values are category types.

- Sample: `curl http://127.0.0.1:5000/questions` 

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```

#### DELETE /questions/<question_id>
- Deletes a specific trivia question based on the provided question_id.
- URL Parameters:
  - question_id (integer): ID of the question to be deleted.
- Returns:
  - success: boolean indicating the success of the deletion operation.
  - deleted: ID of the deleted question.
  - total_questions: total number of remaining questions after deletion.

- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/2`

```
{
  "deleted": 2,
  "success": true,
  "total_questions": 18
}

```

#### POST /questions
- Adds a new trivia question to the database.
- Request Body:
  - question (string): The text of the question.
  - answer (string): The answer to the question.
  - category (integer): The ID of the category to which the question belongs.
  - difficulty (integer): The difficulty level of the question (1-5).
- Returns:
  - success: boolean indicating the success of the operation.
  - created: ID of the newly created question.
  - total_questions: total number of questions after adding the new question.
  - questions: current count of questions.

- Sample: `curl -X POST -H "Content-Type: application/json" -d '{
    "question": "What is the capital of Saudi Arabia?",
    "answer": "riyadh",
    "category": 3,
    "difficulty": 2
}' http://127.0.0.1:5000/questions`

```
{
  "created": 24,
  "success": true,
  "total_questions": 19
}

```

#### POST /questions/search
- Searches for trivia questions containing a given search term.
- Request Body:
  - searchTerm (string): The term to search for in question text.
- Returns:
  - success: boolean indicating the success of the operation.
  - questions: list of trivia questions matching the search term.
  - total_questions: total number of questions matching the search term.

- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "Saudi"}' http://127.0.0.1:5000/questions/search`

```
{
  "questions": [
    {
      "answer": "riyadh",
      "category": 3,
      "difficulty": 2,
      "id": 24,
      "question": "What is the capital of Saudi Arabia?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

#### GET /categories/<int:category_id>/questions
- Retrieves trivia questions associated with a specific category.
- Parameters:
  - category_id (integer): ID of the category for which questions are to be retrieved.
- Returns:
  - success: boolean indicating the success of the operation.
  - questions: list of trivia questions associated with the specified category.
  - total_questions: total number of questions associated with the category.
  - current_category: ID of the category for which questions are retrieved.

- Sample: `curl http://127.0.0.1:5000/categories/3/questions`

```
{
  "current_category": 3,
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "riyadh",
      "category": 3,
      "difficulty": 2,
      "id": 24,
      "question": "What is the capital of Saudi Arabia?"
    }
  ],
  "success": true,
  "total_questions": 4
}
```
#### POST /quizzes
- Initiates a quiz by selecting a random question from a specified category or from all categories.
- Parameters:
  - previous_questions (list): List of question IDs already presented to the user.
  - quiz_category (dict): Dictionary containing 'id' of the category from which questions should be selected. If id is 0, questions are selected from all categories.
- Returns:
  - success: boolean indicating the success of the operation.
  - question: a single trivia question selected randomly based on the specified category or all categories.

- Sample: `curl -X POST -H "Content-Type: application/json" -d '{
    "previous_questions": [5, 8],
    "quiz_category": {"id": 4, "type": "History"}
}' http://127.0.0.1:5000/quizzes`

```
{
  "question": {
    "answer": "Scarab",
    "category": 4,
    "difficulty": 4,
    "id": 23,
    "question": "Which dung beetle was worshipped by the ancient Egyptians?"
  },
  "success": true
}
```

## Deployment N/A

## Authors
Yours truly, Hana 

## Acknowledgements 
The awesome team at Udacity 