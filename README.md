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

###### General

This endpoint is used to retrieve the details of a specific movie, identified by the `id` URL parameter.

###### Request Body

The endpoint requires an empty request body.

###### Response Body

The endpoint responds with a boolean value of `true` with the index `success` and a list consisting of the one movie whose `id` matches the `id` specified in the request. The index of the list is `movies`.

###### Sample URL

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

###### General

This endpoint is used to create a new `movie`.

###### Request Body

The endpoint requires a `movie` json object with attributes `title` and `release_date` where `release_date` is a valid date.

###### Response Body

The endpoint responds with a json object that contains the id of the created movie under the index `created`, a value of `true` under the index `success` to indicate that the operation was performed successfully, and a list indexed `movies` that contains a single `movie`; the `movie` that has just been created.

###### Sample URL

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" -H 'Content-Type:application/json' -d '
{"title":"Terminator: Salvation","release_date":"2009-05-29T18:25:43.511Z"}'  http://127.0.0.1:5000/movies
```

```json
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

###### General

This endpoint is used to modify the values of the attributes of a movie.

###### Request Body

The endpoint requires a json object consisting of the `title` and `release_date`. If one of the values is not being changed, the current value should be used.

###### Response Body

The endpoint responds with a json object that consists of the `id` of the modified movie under the index `modified`, a boolean value of `true` under the index `success` indicating that no problems were encountered during the operation, and a list indexed `movies` that contains the details of the movie after the modification.

###### Sample URL

```bash
curl -X PATCH -H "Authorization: Bearer $TOKEN" -H 'Content-Type:application/json' -d '{"title":"Terminator: Salvation","release_date":"2009-05-14T18:25:43.511Z"}'  http://127.0.0.1:5000/movies/24
```

```json
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

###### General

This endpoint is used to delete a movie.

###### Request Body

The endpoint requires an empty body.

###### Respose Body

The endpoint responds with a json object consisting of the `id` of the deleted movie under the index `movie`, a boolean value of `true` under the index `success` and an empty list indexed `movies`.

###### Sample URL

```bash
curl -X DELETE -H "Authorization: Bearer $TOKEN"  http://127.0.0.1:5000/movies/24
```

```json
{
  "deleted": 24,
  "movies": [],
  "success": true
}
```

#### Genders

##### GET /genders

###### General

This endpoint is used to retrieve a list of genders.

###### Request Body

The endpoint requires an empty request body.

###### Response Body

The endpoint responds with a list of genders under the index `genders` and a boolean value of `true` under the index `success` indicating that there were no errors while generating the response.

###### Sample URL

```bash
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/genders
```

```json
{
  "genders": [
    {
      "id": 1,
      "name": "Male"
    },
    {
      "id": 2,
      "name": "Female"
    }
  ],
  "success": true
}
```

##### GET /genders/{int}

###### General

This endpoint is used to retrieve the details of a specific gender, identified by the `id` URL parameter.

###### Request Body

The endpoint requires an empty request body.

###### Response Body

The endpoint responds with a boolean value of `true` with the index `success` and a list consisting of the one gender whose `id` matches the `id` specified in the request URL parameter. The index of the list is `genders`.

###### Sample URL

```bash
  curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/genders/2
```

```json
{
  "genders": [
    {
      "id": 2,
      "name": "Female"
    }
  ],
  "success": true
}
```

##### POST /genders

###### General

This endpoint is used to create a new `gender`.

###### Request Body

The endpoint requires a `gender` json object with the single attribute `name`.

###### Response Body

The endpoint responds with a json object that contains the id of the created gender under the index `created`, a value of `true` under the index `success` to indicate that the operation was performed successfully, and a list indexed `genders` that contains a single `gender`; the `gender` that has just been created.

###### Sample URL

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type:application/json" -d '{"name":"Prefer not to say."}' http://127.0.0.1:5000/genders
```

```json
{
  "created": 4,
  "genders": [
    {
      "id": 4,
      "name": "Prefer not to say."
    }
  ],
  "success": true
}
```

##### PATCH /genders/{int}

###### General

This endpoint is used to modify the value of the `name` attribute of a gender.

###### Request Body

The endpoint requires a json object consisting of the `name`.

###### Response Body

The endpoint responds with a json object that consists of the `id` of the modified gender under the index `modified`, a boolean value of `true` under the index `success` indicating that no problems were encountered during the operation, and a list indexed `genders` that contains the details of the gender after the modification.

###### Sample URL

```bash
curl -X PATCH -H "Authorization: Bearer $TOKEN" -H "Content-Type:application/json" -d '{"name":"UnKnown"}' http://127.0.0.1:5000/genders/4
```

```json
{
  "genders": [
    {
      "id": 4,
      "name": "UnKnown"
    }
  ],
  "modified": 4,
  "success": true
}
```

##### DELETE /genders/{int}

###### General

This endpoint is used to delete a gender.

###### Request Body

The endpoint requires an empty body.

###### Respose Body

The endpoint responds with a json object consisting of the `id` of the deleted gender under the index `gender`, a boolean value of `true` under the index `success` and an empty list indexed `genders`.

###### Sample URL

```bash
  curl -X DELETE -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/genders/4
```

```json
{
  "deleted": 4,
  "genders": [],
  "success": true
}
```

#### Actors

##### GET /actors

###### General

This endpoint is used to retrieve a list of actors.

###### Request Body

The endpoint requires an empty request body.

###### Response Body

The endpoint responds with a list of actors under the index `actors` and a boolean value of `true` under the index `success` indicating that there were no errors while generating the response.

###### Sample URL

```bash
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/actors
```

```json
{
  "actors": [
    {
      "age": 41,
      "dob": "Fri, 28 Dec 1979 18:25:43 GMT",
      "gender": "Female",
      "id": 1,
      "name": "Noomi Rapace"
    },
    {
      "age": 66,
      "dob": "Tue, 28 Dec 1954 18:25:43 GMT",
      "gender": "Male",
      "id": 2,
      "name": "Denzel Washington"
    },
    {
      "age": 46,
      "dob": "Mon, 11 Nov 1974 18:25:43 GMT",
      "gender": "Male",
      "id": 3,
      "name": "Leonardo DiCaprio"
    }
  ],
  "success": true
}
```

##### GET /actors/{int}

###### General

This endpoint is used to retrieve the details of a specific actor, identified by the `id` URL parameter.

###### Request Body

The endpoint requires an empty request body.

###### Response Body

The endpoint responds with a boolean value of `true` with the index `success` and a list consisting of the one actor whose `id` matches the `id` specified in the request URL parameter. The index of the list is `actors`.

###### Sample URL

```bash
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/actors/1
```

```json
{
  "actors": [
    {
      "age": 41,
      "dob": "Fri, 28 Dec 1979 18:25:43 GMT",
      "gender": "Female",
      "id": 1,
      "name": "Noomi Rapace"
    }
  ],
  "success": true
}
```

##### POST /actors

###### General

This endpoint is used to create a new `actor`.

###### Request Body

The endpoint requires a `actor` json object with the attributes `name`, the date of birth `dob` and the gender `id` `gender_id`.

###### Response Body

The endpoint responds with a json object that contains the id of the created actor under the index `created`, a value of `true` under the index `success` to indicate that the operation was performed successfully, and a list indexed `actors` that contains a single `actor`; the `actor` that has just been created.

###### Sample URL

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type:application/json" -d '{"name":"Linda Hamilton", "dob":
"1956-09-26T00:00:00.000Z","gender_id":"2"}' http://127.0.0.1:5000/actors
```

```json
{
  "actors": [
    {
      "age": 65,
      "dob": "Wed, 26 Sep 1956 00:00:00 GMT",
      "gender": "Female",
      "id": 5,
      "name": "Linda Hamilton"
    }
  ],
  "created": 5,
  "success": true
}
```

##### PATCH /actors/{int}

###### General

This endpoint is used to modify the value of the attributes of an actor.

###### Request Body

The endpoint requires a json object consisting of the `name`, `dob` and `gender_id` attributes of an actor.

###### Response Body

The endpoint responds with a json object that consists of the `id` of the modified actor under the index `modified`, a boolean value of `true` under the index `success` indicating that no problems were encountered during the operation, and a list indexed `actors` that contains the details of the actor after the modification.

###### Sample URL

```bash
curl -X PATCH -H "Authorization: Bearer $TOKEN" -H "Content-Type:application/json" -d '{"name":"Linda Carroll
Hamilton", "dob":"1956-09-26T00:00:00.000Z","gender_id":"2"}' http://127.0.0.1:5000/actors/5
```

```json
{
  "actors": [
    {
      "age": 65,
      "dob": "Wed, 26 Sep 1956 00:00:00 GMT",
      "gender": "Female",
      "id": 5,
      "name": "Linda Carroll Hamilton"
    }
  ],
  "modified": 5,
  "success": true
}
```

##### DELETE /actors/{int}

###### General

This endpoint is used to delete an actor.

###### Request Body

The endpoint requires an empty body.

###### Respose Body

The endpoint responds with a json object consisting of the `id` of the deleted actor under the index `actor`, a boolean value of `true` under the index `success` and an empty list indexed `actors`.

###### Sample URL

```bash
curl -X DELETE -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/actors/6
```

```json
{
  "actors": [],
  "deleted": 6,
  "success": true
}
```

#### Castings

##### GET /castings

###### General

This endpoint is used to retrieve a list of castings.

###### Request Body

The endpoint requires an empty request body.

###### Response Body

The endpoint responds with a list of castings under the index `castings` and a boolean value of `true` under the index `success` indicating that there were no errors while generating the response.

###### Sample URL

```bash
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/castings
```

```json
{
  "castings": [
    {
      "actor": "Noomi Rapace",
      "casting_date": "Wed, 01 Aug 2012 18:25:43 GMT",
      "id": 1,
      "movie": "Alien:Covenant",
      "recast_yn": "N"
    },
    {
      "actor": "Denzel Washington",
      "casting_date": "Mon, 02 Feb 2004 18:25:43 GMT",
      "id": 8,
      "movie": "Deja Vu",
      "recast_yn": "N"
    }
  ],
  "success": true
}
```

##### GET /castings/{int}

###### General

This endpoint is used to retrieve the details of a specific casting, identified by the `id` URL parameter.

###### Request Body

The endpoint requires an empty request body.

###### Response Body

The endpoint responds with a boolean value of `true` with the index `success` and a list consisting of the one casting whose `id` matches the `id` specified in the request URL parameter. The index of the list is `castings`.

###### Sample URL

```bash
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/castings/1
```

```json
{
  "castings": [
    {
      "actor": "Noomi Rapace",
      "casting_date": "Wed, 01 Aug 2012 18:25:43 GMT",
      "id": 1,
      "movie": "Alien:Covenant",
      "recast_yn": "N"
    }
  ],
  "success": true
}
```

##### POST /castings

###### General

This endpoint is used to create a new `casting`.

###### Request Body

The endpoint requires a `casting` json object with the attributes `actor_id`, `movie_id` and the casting date `casting_date`. There is also an optional parameter called `recast_yn` which takes on a default value of `false` if not specified in the request.

###### Response Body

The endpoint responds with a json object that contains the id of the created casting under the index `created`, a value of `true` under the index `success` to indicate that the operation was performed successfully, and a list indexed `castings` that contains a single item; the `casting` that has just been created.

###### Sample URL

```bash
 curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type:application/json" -d '{"actor_id":"5","movie_id":"36","casting_date":"1990-05-10T00:00:00.000Z"}' http://127.0.0.1:5000/castings
```

```json
{
  "castings": [
    {
      "actor": "Linda Carroll Hamilton",
      "casting_date": "Thu, 10 May 1990 00:00:00 GMT",
      "id": 9,
      "movie": "Terminator 2: Judgment Day",
      "recast_yn": "N"
    }
  ],
  "created": 9,
  "success": true
}
```

##### PATCH /castings/{int}

###### General

This endpoint is used to modify the value of the attributes of a casting.

###### Request Body

The endpoint requires a json object consisting of the `actor_id`, `movie_id` and `casting_date`. As in POST above, `recast_yn` is optional and defaults to the current value if a new value is not provided.

###### Response Body

The endpoint responds with a json object that consists of the `id` of the modified casting under the index `modified`, a boolean value of `true` under the index `success` indicating that no problems were encountered during the operation, and a single item list indexed `castings` that contains the details of the modified casting after the changes are applied.

###### Sample URL

```bash
curl -X PATCH -H "Authorization: Bearer $TOKEN" -H "Content-Type:application/json" -d '{"actor_id":"5","movie_id":"36","casting_date":"1990-07-15T00:00:00.000Z"}' http://127.0.0.1:5000/castings/9
```

```json
{
  "castings": [
    {
      "actor": "Linda Carroll Hamilton",
      "casting_date": "Sun, 15 Jul 1990 00:00:00 GMT",
      "id": 9,
      "movie": "Terminator 2: Judgment Day",
      "recast_yn": "N"
    }
  ],
  "modified": 9,
  "success": true
}
```

##### DELETE /castings/{int}

###### General

This endpoint is used to delete a casting.

###### Request Body

The endpoint requires an empty body.

###### Respose Body

The endpoint responds with a json object consisting of the `id` of the deleted casting under the index `casting`, a boolean value of `true` under the index `success` and an empty list indexed `castings`.

###### Sample URL

```bash
curl -X DELETE -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/castings/10
```

```json
{
  "castings": [],
  "deleted": 10,
  "success": true
}
```

## Deployment

The application will be deployed to Heroku.

## Authors

Most of the code was written by Gift Chimphonda. A lot of it was based on starter code from Udacity. And Stack Overflow helped when troubleshooting errors.
 
## Acknowledgements

The following threads on Stack Overflow helped during key parts of the development process:

[What is the right JSON Date Format?](https://stackoverflow.com/questions/10286204/what-is-the-right-json-date-format)

[How to run unittest main for all source files in a subdirectory](https://stackoverflow.com/questions/644821/python-how-to-run-unittest-main-for-all-source-files-in-a-subdirectory)

[datetime — Basic date and time types](https://docs.python.org/3/library/datetime.html)


