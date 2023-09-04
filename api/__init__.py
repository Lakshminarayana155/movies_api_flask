from flask import Flask
from flask_restx import Api
from .auth.views import auth_namespace
from .movies.views import movies_namespace
from .config.config import config_dict
from .utils.__init__ import db
from .models.users import User
from .models.movies import Movie
from flask_migrate import Migrate 
from flask_jwt_extended import JWTManager


def createapp(conf=config_dict['dev']):
    app=Flask(__name__)

    #setting configuration from the specified configuration object
    app.config.from_object(conf)

    api=Api(app)
    #adding the movies and authentication namespaces to the API
    api.add_namespace(movies_namespace)
    api.add_namespace(auth_namespace,path='/auth')

    db.init_app(app)
    #setting Flask-JWT-Extended extension with the app
    jwt=JWTManager(app)
    #Migrate instance to manage database migrations
    migrate=Migrate(app,db)

    #shell context processor to provide objects in the Flask shell
    @app.shell_context_processor
    def make_shell_context():
        return{
            'db':db,
            'User': User,
            'Movie': Movie,
        }

    return app