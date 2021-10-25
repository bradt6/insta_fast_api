## Start the app
* The app can be started by using docker-compose up --build
* The apps docs can be found at http://0.0.0.0:8888/docs

## The api docs can be found at URL
* Get user by id. http://0.0.0.0:8888/users/1 -> id is an int 
	* This will fetch the user with the id specified.
* There are 2 endpoints one with a list all users with 2 query parameters one with a skip(offset) and one with the query limit. This is set to a max of 100 to keep load times optimal. There is a continuation  token sent back in the response for say next page functionality. This could be used with the frontend, to list the users with a cap of 100 with a page number associated the corresponding prefixed digit. This could also be integrated in some type of Ajax call for infinite scroll functionality. All params are integers 
	* localhost:8000/users?skip={skip_val}&limit={limit_val}'
	* http://0.0.0.0:8888/users?next_page_token={next_page_val}&skip=0&limit={limit}
	* http://0.0.0.0:8888/users?before_page_token={before_val}&skip=0&limit={limit_val}

## Tests 
- tests can be run by accessing the docker container. In terminal - docker ps
	- copy the container id 
	- copy the container id into the below command.
	- docker exec -it CONTAINER_ID pytest tests.py

## Considerations
* Pagination should be done with the Keyset pagination. This is because when we offset the program must first look up all the prior entries to get to this offset amount. This isn't very performant when dealing with large data sets. 
	* There is no back token integrated into this solution
* Integrate caching to make previous queries more performant
* Introduce streams and chunks of data for querying large amounts of data
* Wouldn't use Int in a production system 
	* UUID should be used in a production system as we can almost guarantee there will be no clash. 
	* Avoid the chances of a clash with further system which may be integrated onto the platform by acquisition or collaboration 
	* When models use AUTO_increment auto we require a round trip from the database and the app to acquire the next relevant id. This	 carries a  performance cost. 
	* UUID are also much better suited for distributed systems as each Microservice will carry its own database thus minimising the issue with clashes and Uuid can be instantiated at time when its needed 


## Production 
* Authentication token when sending api requests 
* Use Keyset pagination 
	* avoid using offset value as this iterates through the items until it reaches the target.
* Can implement the continuation token in Headers minimising the data in the returned JSON.  
