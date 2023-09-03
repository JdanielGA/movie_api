from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.users import users_router

# Create the FastAPI instance.
app = FastAPI()
app.title = 'Movie Description with FastAPI'
app.description = 'This is a simple API that returns movie description'
app.version = '0.0.2'

# Add the error handler middleware.
app.add_middleware(ErrorHandler)

# Create the database tables.
Base.metadata.create_all(bind=engine)

# Include the user router.
app.include_router(users_router)

# Include the movie router.
app.include_router(movie_router)

# Function to get the home page.
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