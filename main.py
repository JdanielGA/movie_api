from fastapi import FastAPI, Path, Query, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from typing import List, Dict
from starlette.requests import Request
from models.movies import MovieModel, Movie
from models.users import User
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import session, engine, Base


app = FastAPI()
app.title = 'Movie Description with FastAPI'
app.description = 'This is a simple API that returns movie description'
app.version = '0.0.2'

Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'admin@email.com':
            raise HTTPException(status_code=403, detail='Invalid credentials')


@app.get('/', tags=['home'])
def home_page():
    message = HTMLResponse("""
    <html>
        <head>
            <title>Movie Description API</title>
        </head>
        <body>
            <h1>Welcome to the Movie Description API</h1>
            <p>Use the <a href="/docs">/docs</a> endpoint to view the documentation</p>
        </body>
    </html>
    """)
    return message

# Function to do user login.
@app.post('/login', tags=['auth'], status_code=200)
def login(user: User):
    if user.email == 'admin@email.com' and user.password == 'password':
        token: str = create_token(user.model_dump())        # Create a token.
        return {'token': token}
    raise HTTPException(status_code=401, detail='Invalid email or password')

# Function to get all movies in our database.
@app.get('/movies', tags=['movies'], response_model=List[Movie], dependencies=[Depends(JWTBearer())])
def list_movies(): 
    db = session()                                          # Create a database session.
    list_movies = db.query(MovieModel).all()                # Get all movies from the database.
    return list_movies    

# Function to get a movie by ID.
@app.get('/movies/{movie_id}', tags=['movies'], response_model=Movie, dependencies=[Depends(JWTBearer())])
def get_by_id(movie_id: int = Path(ge = 0, description='The ID of the movie you want to retrieve.')):
    db = session()                                          # Create a database session.
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()   # Get the movie from the database usising filter from SQLAlchemy and show the first result.
    if movie:
        return movie
    raise HTTPException(status_code=404, detail={'message': 'Movie not found.'})

# Funtion to get movies by category.
@app.get('/movies/category/{category}', tags=['movies'], response_model=List[Movie], dependencies=[Depends(JWTBearer())])
def get_by_category(category: str = Path(description='The category of the movie you want to retrieve.')):
    db = session()                                          # Create a database session.
    movies = db.query(MovieModel).filter(MovieModel.category == category).all()  # Get the movies from the database usising filter from SQLAlchemy and show all results.
    if movies:
        return movies
    raise HTTPException(status_code=404, detail={'message': 'Any movie was found with this category.'})


# Function to create a new movie in our database.
@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie):
    try:
        movie = MovieModel(**movie.model_dump())            # Create a movie object.
        db = session()                                      # Create a database session.
        db.add(movie)                                       # Add the movie to the database.
        db.commit()                                         # Save the changes.
        return {'message': 'Movie created successfully.'}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail={'message': 'Internal server error.'})