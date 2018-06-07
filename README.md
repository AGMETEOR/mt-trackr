### Maintenance-Tracker APP API

[![Build Status](https://travis-ci.org/AGMETEOR/mt-trackr.svg?branch=develop)](https://travis-ci.org/AGMETEOR/mt-trackr)

[![Coverage Status](https://coveralls.io/repos/github/AGMETEOR/mt-trackr/badge.svg?branch=develop)](https://coveralls.io/github/AGMETEOR/mt-trackr?branch=develop)



Maintenance Tracker App is an application that provides users with the ability to reach out to operations or repairs department regarding repair or maintenance requests and monitor the status of their request.

## Prerequisites
> $ pip install -r requirements.txt 

## Run

> $ python manage.py runserver 

## Testing
> $ nosetests

## API End Points

| End Point  | Description |
| ------------- | ------------- |
| POST /auth/signup  | Register a user  |
| POST /auth/login  | Login a user  |
| GET /users/requests | Fetch all the requests of a logged in user |
| GET /users/requests/<requestId>/ |  Fetch a request that belongs to a logged in user |
| POST /users/requests |Create a request |
| PUT /users/requests/<requestId> |Modify a request |
| Get /requests/   | Fetch all the requests. Available to only admin |
| PUT /requests/<requestId>/approve/ | Approve request. This is available only to admin users. When this endpoint is called, the status of the request should be pending.|
|PUT /requests/<requestId>/disapprove |Disapprove request. This is available only to admin users. |
| PUT /requests/<requestId>/resolve | Resolve request. This is available only to admin users. |
