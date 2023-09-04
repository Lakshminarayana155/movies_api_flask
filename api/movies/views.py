from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from ..models.movies import Movie
from http import HTTPStatus
from ..utils.__init__ import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.users import User


movies_namespace=Namespace('movies',description="a namespace for movies")

movie_model=movies_namespace.model(
    'Movie',{
        'id':fields.Integer(),
        'title':fields.String(required=True, description='title'),
        'director':fields.String(required=True, description='director'),
        'rating':fields.Float(required=True, description='rating'),
        'year':fields.Integer(required=True, description='year'),
        'genre':fields.String(required=True, description='genere'),
        'description':fields.String(description='description')
    }
)

search_model = movies_namespace.model('MovieSearch', {
    'title': fields.String(description='Movie title'),
    'director': fields.String(description='Director name'),
    'year': fields.Integer(description='Release year'),
    'genre': fields.String(description='Movie genre'),
})

@movies_namespace.route("/")
class MovieAddGet(Resource):
    @movies_namespace.marshal_with(movie_model)
    def get(self):
        """
        Get all movies (all_users)
        """
        movies= Movie.query.all()

        return movies, HTTPStatus.OK
    
    
    @movies_namespace.expect(movie_model)
    @movies_namespace.marshal_with(movie_model)
    @jwt_required()
    def post(self):
        """
        Add a movie (Admin_user)
        """
        current_user_id = get_jwt_identity()  # Get the current user's identity (user_id)
        user = User.get_by_id(current_user_id)
        if user.is_staff==True:
            data = movies_namespace.payload

            new_movie=Movie(
                title=data['title'],
                director=data['director'],
                rating=data['rating'],
                year=data['year'],
                genre=data['genre'],
                description=data['description']
            )

            new_movie.save()

            return new_movie, HTTPStatus.CREATED
        else:
            return "Only staff can delete user data", HTTPStatus.OK
        

@movies_namespace.route("/<int:movie_id>")
class GetUpdateDelete(Resource):

    @movies_namespace.marshal_with(movie_model)
    def get(self,movie_id):
        """
        Retrive movie using id (All_users)
        """
        movie= Movie.get_by_id(movie_id)
        return movie, HTTPStatus.OK

    @movies_namespace.expect(movie_model)
    @movies_namespace.marshal_with(movie_model)
    @jwt_required()
    def put(self,movie_id):
        """
        update movie using id (Admin_user)
        """
        current_user_id = get_jwt_identity()  # Get the current user's identity (user_id)
        user = User.get_by_id(current_user_id)
        if user.is_staff==True:
            movie_to_update= Movie.get_by_id(movie_id)
            data= movies_namespace.payload

            movie_to_update.title=data['title']
            movie_to_update.director=data['director']
            movie_to_update.rating=data['rating']
            movie_to_update.year=data['year']
            movie_to_update.genre=data['genre']
            movie_to_update.description=data['description']

            db.session.commit()
            return movie_to_update, HTTPStatus.OK
        else:
            return "Only staff can see all users", HTTPStatus.OK
        

    @movies_namespace.expect(movie_model)
    @movies_namespace.marshal_with(movie_model)
    @jwt_required()
    def patch(self, movie_id):
        """
        Partially update movie using id (Admin_user)
        """
        current_user_id = get_jwt_identity()  # Get the current user's identity (user_id)
        user = User.get_by_id(current_user_id)
        if user.is_staff==True:
            movie_to_update = Movie.get_by_id(movie_id)
            data= movies_namespace.payload

            # Update only the fields that are provided in the request
            if 'title' in data:
                movie_to_update.title = data['title']
            if 'director' in data:
                movie_to_update.director = data['director']
            if 'rating' in data:
                movie_to_update.rating = data['rating']
            if 'year' in data:
                movie_to_update.year = data['year']
            if 'genre' in data:
                movie_to_update.genre = data['genre']
            if 'description' in data:
                movie_to_update.description = data['description']

            db.session.commit()
            return movie_to_update, HTTPStatus.OK
        else:
            return "Only staff can see all users", HTTPStatus.OK
        
    
    @movies_namespace.marshal_with(movie_model)
    @jwt_required()
    def delete(self,movie_id):
        """
        delete movie using id (Admin_user)
        """
        current_user_id = get_jwt_identity()  # Get the current user's identity (user_id)
        user = User.get_by_id(current_user_id)
        if user.is_staff==True:
            movie_to_update= Movie.get_by_id(movie_id)
            movie_to_update.delete()

            return movie_to_update, HTTPStatus.NO_CONTENT
        else:
            return "Only staff can see all users", HTTPStatus.OK
        
@movies_namespace.route("/search")
class MovieSearch(Resource):
    @movies_namespace.expect(search_model)
    @movies_namespace.marshal_list_with(movie_model)
    def post(self):
        """
        Search for movies based on criteria (title, director, year, genre) (All_users)
        """
        try:
            search_params = movies_namespace.payload
            movies = Movie.query.filter_by(**search_params).all()

            return movies, HTTPStatus.OK
        except Exception as e:
            return "Something is wrong"