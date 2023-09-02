from fastapi import FastAPI, Path, Query, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from typing import List, Dict
from starlette.requests import Request
from models.movies import Movie
from models.users import User
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer


app = FastAPI()
app.title = 'Movie Description with FastAPI'
app.description = 'This is a simple API that returns movie description'
app.version = '0.0.1'


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'admin@email.com':
            raise HTTPException(status_code=403, detail='Invalid credentials')


films = [
    {
        'id': 1,
        'title': 'Titanic',
        'overview': 'A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.',
        'year': 1997,
        'rating': 7.8,
        'category': 'Drama'
    },
    {
        'id': 2,
        'title': 'The Avengers: Endgame',
        'overview': 'After the devastating events of Avengers: Infinity War (2018), the universe is in ruins.',
        'year': 2019,
        'rating': 8.4,
        'category': 'Action'
    },
    {
        'id': 3,
        'title': 'Lord of the Rings: The fellowship of the ring',
        'overview': 'A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.',
        'year': 2001,
        'rating': 8.8,
        'category': 'Fantasy'
    },
    {
        'id': 4,
        'title': 'The Matrix',
        'overview': 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.',
        'year': 1999,
        'rating': 8.7,
        'category': 'Sci-Fi'
    },
    {
        'id': 5,
        'title': 'Harry Potter and the goblet of fire',
        'overview': 'Harry Potter finds himself competing in a hazardous tournament between rival schools of magic, but he is distracted by recurring nightmares.',
        'year': 2005,
        'rating': 7.7,
        'category': 'Fantasy'
    }
]


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

@app.post('/login', tags=['auth'], status_code=200)
def login(user: User):
    if user.email == 'admin@email.com' and user.password == 'password':
        token: str = create_token(user.model_dump())
        return {'token': token}
    raise HTTPException(status_code=401, detail='Invalid email or password')
    

@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies():
    if len(films) == 0:
        raise HTTPException(status_code=404, detail='No movies found')    
    return films 


@app.get('/movies/{movie_id}', tags=['movies'], response_model=Movie, status_code=200)
def get_movie_by_id(movie_id: int = Path(ge=0, le=100, description='The ID of the movie you want to view')):
    for movie in films:
        if movie['id'] == movie_id:
            return movie
    raise HTTPException(status_code=404, detail='Movie not found')

@app.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length=2, max_length=50)):
    movies = []
    for movie in films:
        if movie['category'].lower() == category.lower():
            movies.append(movie)
    raise HTTPException(status_code=404, detail='No movies found')

@app.post('/movies', tags=['movies'], response_model=Dict, status_code=201)
def add_movie(movie: Movie):
    try:
        films.append(movie.model_dump())
    except:
        raise HTTPException(status_code=400, detail='Invalid movie data')
    return {'Success': 'Movie added successfully'}

@app.put('/movies/{movie_id}', tags=['movies'], response_model=Dict, status_code=200)
def update_movie(movie_id: int = Path(ge=0, le=100, description='The ID of the movie you want to update'), movie: Movie = None):
    for i in range(len(films)):
        if films[i]['id'] == movie_id:
            films[i] = movie.model_dump()
            return {'Success': 'Movie updated successfully'}
    raise HTTPException(status_code=404, detail={'Error': 'Movie not found'})

@app.delete('/movies/{movie_id}', tags=['movies'], response_model=Dict, status_code=200)
def delete_movie(movie_id: int = Path(ge=1, le=100, description='The ID of the movie you want to delete')):
    for i in range(len(films)):
        if films[i]['id'] == movie_id:
            del films[i]
            return {'Success': 'Movie deleted successfully'}
    raise HTTPException(status_code=404, detail={'Error': 'Movie not found'})