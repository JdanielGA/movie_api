from fastapi import APIRouter, Path, HTTPException, Depends
from typing import List
from models.movies import MovieModel
from config.database import session
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()

# Function to get all movies in our database.
@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], dependencies=[Depends(JWTBearer())])
def list_movies(): 
    db = session()                                          # Create a database session.
    list_movies = MovieService(db).get_movies()            # Get all movies from the database using the service.
    return list_movies    

# Function to get a movie by ID.
@movie_router.get('/movies/{movie_id}', tags=['movies'], response_model=Movie, dependencies=[Depends(JWTBearer())])
def get_by_id(movie_id: int = Path(ge = 0, description='The ID of the movie you want to retrieve.')):
    db = session()                                          # Create a database session.
    movie = MovieService(db).get_movie_by_id(movie_id)   # Get the movie from the database usising filter from SQLAlchemy and show the first result.
    if movie:
        return movie
    raise HTTPException(status_code=404, detail={'message': 'Movie not found.'})

# Funtion to get movies by category.
@movie_router.get('/movies/category/{category}', tags=['movies'], response_model=List[Movie], dependencies=[Depends(JWTBearer())])
def get_by_category(category: str = Path(description='The category of the movie you want to retrieve.')):
    db = session()                                          # Create a database session.
    movies = MovieService(db).get_movie_by_category(category)  # Get the movies from the database usising filter from SQLAlchemy and show all results.
    if movies:
        return movies
    raise HTTPException(status_code=404, detail={'message': 'Any movie was found with this category.'})


# Function to create a new movie in our database.
@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201, dependencies=[Depends(JWTBearer())])
def create_movie(movie: Movie):
    try:
        db = session()                                          # Create a database session.
        if MovieService(db).get_movie_by_id(movie.id):          # Check if the movie already exists.
            return {'message': 'Movie already exists.'}
        else:
            MovieService(db).create_movie(movie)                # Create the movie.
            return {'message': 'Movie created successfully.'}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail={'message': 'Internal server error.'})
    
# Function to update a movie in our database.
@movie_router.put('/movies/{movie_id}', tags=['movies'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def update_movie(movie_id: int = Path(ge = 0, description='The ID of the movie you want to update.'), movie: Movie = None):
    try:
        db = session()  # Create a database session.
        result = MovieService(db).update_movie(movie_id, movie)
        if result:
            return {'message': 'Movie updated successfully.'}
        else:
            raise HTTPException(status_code=404, detail={'message': 'Movie not found.'})
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail={'message': 'Internal server error.'})

# Function to delete a movie in our database.
@movie_router.delete('/movies/{movie_id}', tags=['movies'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def delete_movie(movie_id: int = Path(ge = 0, description='The ID of the movie you want to delete.')):
    try:
        db = session()  # Create a database session.
        result = MovieService(db).delete_movie(movie_id)
        if result:
            return {'message': 'Movie deleted successfully.'}
        else:
            raise HTTPException(status_code=404, detail={'message': 'Movie not found.'})
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail={'message': 'Internal server error.'})