"""
Routes and views for the bottle application.
"""

from bottle import route, view
from datetime import datetime

@route('/')
@route('/home')
@view('index')
def home():
    """Renders the home page."""
    return dict(
        year=datetime.now().year
    )

@route('/predator_pray')
@view('predator_pray')
def predator_pray():
    """Renders the predator_pray page."""
    return dict(
        title='Predator-pray',
        message='Your predator-pray page.',
        year=datetime.now().year
    )

@route('/epidemic')
@view('epidemic')
def epidemic():
    """Renders the epidemic page."""
    return dict(
        title='Epidemic',
        message='Your application description page.',
        year=datetime.now().year
    )

@route('/competition')
@view('competition')
def competition():
    """Renders the competition page."""
    return dict(
        title='Competition',
        message='Your application description page.',
        year=datetime.now().year
    )

@route('/fishing')
@view('fishing')
def fishing():
    """Renders the fishing page."""
    return dict(
        title='Fishing',
        message='Your application description page.',
        year=datetime.now().year
    )
