# MOVIE-API - README

## Description
This is a simple API that returns movie data from a database, like the movie title, overview, release date, and the score. Users login to the API to get a token to access the movie data, add new movies, update existing movies, and delete movies.
This application is built with Python, FastAPI, SQLAlchemy, JWT for authentication, and it can be deployed with Docker.

## Installation
1. Make sure you have Python 3.10 or higher installed.
2. Clone the repository.
3. Create a virtual environment.
4. Install the dependencies from the requirements.txt file with the command `pip install -r requirements.txt`.

## Usage
1. Run the command `uvicorn main:app --reload` to start the server.
2. Go to `http://localhost/docs` to view the documentation.
3. The default user email is 'admin@email.com' and the password is 'password' for login. (You can change this).
4. You can use the token generated from the login to access the movie data, add new movies, update existing movies, and delete movies.

## Deployment
1. Make sure you have Docker installed.
2. Use de command: `docker-compose up -d` to start the server.
3. Use do command: `docker-compose ps` to view the running containers.
4. Go to `http://localhost/docs` to view the documentation.
5. For stop the server, use the command: `docker-compose down`.
6. If you want to build the image, you can Run the command `docker build -t movie-api .` to build the image, you can change the name of the image.
7. If you want to run the image, you can Run the command `docker run -d -p 80:80 movie-api` to run the image or you can use Docker desktop to run the image.
8. For stop the image, use the command: `docker stop <container id>` or stop it from Docker desktop.

## Project Structure
- **config**: This folder contains the database configuration.
- **database**: This folder contains the database files 'database.sqlite'.
- **middlewares**: This folder contains the error handler middleware and the JWT authentication.
- **models**: This folder contains the database models for movies.
- **routers**: This folder contains the routers for movies and users.
- **schemas**: This folder contains the schemas for movies and users.
- **routes**: This folder contains the routes for movies and users.
- **utils**: This folder contains the mainly functions for the application of movies.
- **main.py**: This is the main file of the application.
- **requirements.txt**: This file contains the dependencies of the application.
- **Dockerfile**: This file contains the configuration for build the image.
- **docker-compose.yml**: This file contains the configuration for run the image.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Contact
For any questions or inquiries, please contact me.

## License
[MIT](https://choosealicense.com/licenses/mit/)
