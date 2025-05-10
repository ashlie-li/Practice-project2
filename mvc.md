## General API workflow
client ->                       server               <-> db

          HTTP protocol: GET POST PUT DELETE          SQL
          resource endpoints: /api/v1/....            postgres SQL
          implementation language: python, java.      MySQL
          framework: flask, spring boot.               Oracle SQL


                                                      NoSQL
                                                      Mongodb (Document Based)
                                                      DynamoDB


### Server usually use (MVC) framework
1. Models: (ORM(eg: sqlalchemy)) talks to db
2. Views: (HTML, JSON, XML) return response in particular format back to client
3. Controllers: (endpoints, routes) handle request and return response
4. Services: to extract business logic from controllers


### Clients:
1. curl
   - calls endpoints via terminal
2. Postman
  - it's a convenient app similar to curl
3. browsers
  - client side / UI / form
4. http client library programatically
  - from java/python/javascript libraries
  - use case, it can be called by other teams or your scripts 

## AuthN (Authentication) flow:
1. user uses [Postman]
2. make API call to /login with user name and password
3. server query db witn user name and validate password
   - 3a. If it's correct, server generate a token. Server usually returns JSON response with that token with 2xx response code
   - 3b. If it's wrong, deny request, no token issue and server usually returns 4xx response code
5. user uses [Postman] make other api call like GET /api/v1/{resource} with token
6. If token expires, the user would need to repeat step 2
