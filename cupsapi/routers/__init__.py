""" Routes for the application. """
from fastapi import APIRouter

class BaseRouter:
    """ Base router class that imports the APIRouter. """

    def __init__(self):
        self.router = APIRouter()
