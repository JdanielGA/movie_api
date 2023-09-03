from fastapi import APIRouter, Path, HTTPException, Depends
from typing import List
from models.movies import MovieModel, Movie
from config.database import session
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService

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
        movie = MovieModel(**movie.model_dump())            # Create a movie object.
        db = session()                                      # Create a database session.
        db.add(movie)                                       # Add the movie to the database.
        db.commit()                                         # Save the changes.
        return {'message': 'Movie created successfully.'}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail={'message': 'Internal server error.'})
    
# Function to update a movie in our database.
@movie_router.put('/movies/{movie_id}', tags=['movies'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def update_movie(movie_id: int = Path(ge = 0, description='The ID of the movie you want to update.'), movie: Movie = None):
    db = session()                                          # Create a database session.
    movie_to_update = db.query(MovieModel).filter(MovieModel.id == movie_id).first()    # Get the movie from the database usising filter from SQLAlchemy and show the first result.
    if movie_to_update:
        movie_data = movie.model_dump()                     # Get the movie data.
        for key, value in movie_data.items():               # Update the movie data.
            setattr(movie_to_update, key, value)
        db.commit()                                         # Save the changes.
        return {'message': 'Movie updated successfully.'}
    raise HTTPException(status_code=404, detail={'message': 'Movie not found.'})

# Function to delete a movie in our database.
@movie_router.delete('/movies/{movie_id}', tags=['movies'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def delete_movie(movie_id: int = Path(ge = 0, description='The ID of the movie you want to delete.')):
    db = session()                                          # Create a database session.
    movie_to_delete = db.query(MovieModel).filter(MovieModel.id == movie_id).first()    # Get the movie from the database usising filter from SQLAlchemy and show the first result.
    if movie_to_delete:
        db.delete(movie_to_delete)                          # Delete the movie.
        db.commit()                                         # Save the changes.
        return {'message': 'Movie deleted successfully.'}
    raise HTTPException(status_code=404, detail={'message': 'Movie not found.'})