from fastapi import FastAPI

from api.routes import register_routes
from dotenv import load_dotenv

DEBUG = load_dotenv("DEBUG", ) or False

app = FastAPI(
    debug=DEBUG,
    title='Easy APP API',
    docs_url='/api/docs',
)
register_routes(app)
