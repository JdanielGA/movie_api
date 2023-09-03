from models.movies import MovieModel
from schemas.movie import Movie
from fastapi import HTTPException


class MovieService:
    def __init__(self, db) -> None:
        self.db = db

    # Function to get all movies in our database.
    def get_movies(self):
        return self.db.query(MovieModel).all()  # Get all movies from the database using the service.
    
    # Function to get a movie by ID.
    def get_movie_by_id(self, movie_id: int):
        return self.db.query(MovieModel).filter(MovieModel.id == movie_id).first()   # Get the movie from the database usising filter from SQLAlchemy and show the first result.
    
    # Funtion to get movies by category.
    def get_movie_by_category(self, category: str):
        return self.db.query(MovieModel).filter(MovieModel.category == category).all()  # Get the movies from the database usising filter from SQLAlchemy and show all results.
    
    # Function to create a new movie in our database.
    def create_movie(self, movie: Movie):
        new_movie = MovieModel(**movie.model_dump())            # Create a movie object.
        self.db.add(new_movie)                                  # Add the movie to the database.
        self.db.commit()                                        # Save the changes.
        return
    
    # Function to update a movie in our database.
    def update_movie(self, movie_id: int, movie: Movie):
        movie_to_update = self.db.query(MovieModel).filter(MovieModel.id == movie_id).first()    # Get the movie from the database usising filter from SQLAlchemy and show the first result.
        if movie_to_update:
            movie_data = movie.model_dump()                     # Get the movie data.
            for key, value in movie_data.items():               # Update the movie data.
                setattr(movie_to_update, key, value)
            self.db.commit()                                    # Save the changes.
            return True
        return False
    
    # Function to delete a movie in our database.
    def delete_movie(self, movie_id: int):
        movie_to_delete = self.db.query(MovieModel).filter(MovieModel.id == movie_id).first()    # Get the movie from the database usising filter from SQLAlchemy and show the first result.
        if movie_to_delete:
            self.db.delete(movie_to_delete)                     # Delete the movie.
            self.db.commit()                                    # Save the changes.
            return True
        return False