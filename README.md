# Casting API

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)


## Introduction

The Casting API is a web API for casting actors in movies. It is a Flask based API backend designed to be used with a Javascript based frontend client.

The motivation behind its development is to create a simple, secure API for casting actors in movies.

The API code has been written according to pep8 guidelines.

## Getting Started

Install all dependencies by running the following command from the root directory (preferably after creating a virtual environment):

```
pip install -r requirements.txt
```

## Errors



## Resource Endpoint Library

### Movies

#### GET /movies

```
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/movies
```

```
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

#### GET /movies/{int}

```
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/movies/11
```

```
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

#### POST /movies

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

#### PATCH /movies

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

#### DELETE /movies

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
