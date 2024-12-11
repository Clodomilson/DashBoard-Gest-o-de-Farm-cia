from fastapi import FastAPI
from dash import Dash
from fastapi.middleware.wsgi import WSGIMiddleware
from app import app as dash_app  # Importe o seu Dash

server = FastAPI()

# Integre o Dash no FastAPI
server.mount("/", WSGIMiddleware(dash_app.server))
