# Casting API

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

## Introduction

The Casting API is a web API for casting actors in movies. It is a Flask based API backend designed to be used with a Javascript based frontend client.

The motivation behind its development is to create a simple, secure API for casting actors in movies.

The API code has been written according to [pep8 guidelines](http://www.python.org/dev/peps/pep-0008/).

## Getting Started

- Base URL: the API can be accessed at the following URL `http://127.0.0.1:5000`
- Authentication: The API requires a valid AUTH0 Token to accompany every request before access can be granted depending on the access permissions present in the Token.

### Dependencies

Install all dependencies by running the following command from the root directory (preferably inside a virtual environment):

```bash
pip install -r requirements.txt
```

### Databases

The API depends on the presence of a postgresql database, whose name should be properly configured in the `DATABASE_NAME` environment variable.

Unit Tests depend on the presence of a database (preferably a separate database), properly configured in the `TEST_DATABASE_NAME` environment variable.

After both databases (live and test) have been created, update their schema by running migrations against each database.

### Installation

To start the web API; make sure that the database service is running, if it is not yet running; start it using the following command:

```bash
sudo service postgresql start
```

then navigate to the backend directory and run the following commands:

```bash
export DATABASE_NAME={database_name}
export TEST_DATABASE_NAME={test_database_name}
export TEST_MODE={test_mode}
export DATABASE_USER={username}
export DATABASE_PASS={password}
export DATABASE_HOST={hostname}
export DATABASE_PORT={port_number}
export TOKEN={token}
export FLASK_APP=app.py
export FLASK_ENV=development
```

Where:

- `DATABASE_NAME` is the name of the live database
- `TEST_DATABASE_NAME` is the name of the test database
- `TEST_MODE` is a flag taking values `0` (`False`) or `1` (`True`) indicating whether to connect to the test database (if value is `1`) or not (if value is `0`)
- `DATABASE_USER` is the user account used to connect to the database
- `DATABASE_PASS` is the password for the account that is used to connect to the database
- `DATABASE_HOST` is the hostname or IP address of the database server
- `DATABASE_PORT` is the port number of the database service
- `TOKEN` is a valid token

To start the application, run the following command:

```bash
flask run
```

You can then verify that the API is accessible by running the following curl command:

```bash
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/movies
```

## Unit Tests

Unit tests depend on the same environment variables as defined in the [Getting Started](#Getting-Started) section above.
Unit tests have been defined in the `tests` directory but they should be run by running the file `test_app.py` as follows:

```bash
python3 test_app.py
```

## API Reference

### Errors

Errors are returned in the following format:

```json
{
  "success": false,
  "error": 400,
  "message": "bad request"
}
```
Every error response contains a the HTTP status code under the index `error`, a boolean result `false` under the index `success` and a brief message describing the error under the index `message`.

In the event of an error, the API may return one of the following HTTP status codes:
- `404`: not found
- `401`: unauthorized
- `403`: forbidden
- `405`: not allowed
- `422`: unprocessable
- `400`: bad request
- `500`: server error

### Resource Endpoint Library

#### Movies

##### GET /movies

###### General
This endpoint is used to retrieve a list of movies.

###### Request Body
The endpoint requires an empty request body.

###### Response Body
The endpoint responds with a list of movies under the index `movies` and a boolean value of `true` under the index `success` indicating that there were no errors generating the response.

###### Sample URL

```bash
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/movies
```

```json
{
  "movies": [
    {
      "id": 1,
      "release_date": "Sun, 26 Oct 2014 18:25:43 GMT",
      "title": "Interstellar"
    },
    {
      "id": 2,
      "release_date": "Thu, 03 Sep 2020 18:25:43 GMT",
      "title": "Tenet"
    },
    {
      "id": 3,
      "release_date": "Thu, 03 Oct 2013 18:25:43 GMT",
      "title": "Gravity"
    },
    {
      "id": 4,
      "release_date": "Thu, 08 Jul 2010 18:25:43 GMT",
      "title": "Inception"
    },
    {
      "id": 5,
      "release_date": "Fri, 22 Oct 2021 18:25:43 GMT",
      "title": "Dune"
    },
    {
      "id": 6,
      "release_date": "Thu, 11 May 2017 18:25:43 GMT",
      "title": "Alien:Covenant"
    },
    {
      "id": 8,
      "release_date": "Wed, 30 Sep 2015 18:25:43 GMT",
      "title": "The Martian"
    },
    {
      "id": 9,
      "release_date": "Thu, 31 May 2012 18:25:43 GMT",
      "title": "Prometheus"
    },
    {
      "id": 11,
      "release_date": "Wed, 22 Nov 2006 18:25:43 GMT",
      "title": "Deja Vu"
    }
  ],
  "success": true
}
```

##### GET /movies/{int}

```bash
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/movies/11
```

```json
{
  "movies": [
    {
      "id": 11,
      "release_date": "Wed, 22 Nov 2006 18:25:43 GMT",
      "title": "Deja Vu"
    }
  ],
  "success": true
}
```

##### POST /movies

```
curl -X POST -H "Authorization: Bearer $TOKEN" -H 'Content-Type:application/json' -d '
{"title":"Terminator: Salvation","release_date":"2009-05-29T18:25:43.511Z"}'  http://127.0.0.1:5000/movies
```

```
{
  "created": 24,
  "movies": [
    {
      "id": 24,
      "release_date": "Fri, 29 May 2009 18:25:43 GMT",
      "title": "Terminator: Salvation"
    }
  ],
  "success": true
}
```

##### PATCH /movies

```
curl -X PATCH -H "Authorization: Bearer $TOKEN" -H 'Content-Type:application/json' -d '{"title":"Terminator: Salvation","release_date":"2009-05-14T18:25:43.511Z"}'  http://127.0.0.1:5000/movies/24
```

```
{
  "modified": 24,
  "movies": [
    {
      "id": 24,
      "release_date": "Thu, 14 May 2009 18:25:43 GMT",
      "title": "Terminator: Salvation"
    }
  ],
  "success": true
}
```

##### DELETE /movies

```
curl -X DELETE -H "Authorization: Bearer $TOKEN"  http://127.0.0.1:5000/movies/24
```

```
 {
  "deleted": 24,
  "movies": [],
  "success": true
}
```

## Deployment

The application will be deployed to Heroku.

## Authors

## Acknowledgements
