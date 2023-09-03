from models.movies import MovieModel


class MovieService:
    def __init__(self, db) -> None:
        self.db = db

    def get_movies(self):
        return self.db.query(MovieModel).all()
    
    def get_movie_by_id(self, movie_id: int):
        return self.db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    
    def get_movie_by_category(self, category: str):
        return self.db.query(MovieModel).filter(MovieModel.category == category).all()