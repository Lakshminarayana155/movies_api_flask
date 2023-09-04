from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.exceptions import Conflict, BadRequest
from ..utils.__init__ import db

#namespace for authentication-related routes
auth_namespace=Namespace('auth',description="a namespace for authentication")
#models for request and response data
signup_model= auth_namespace.model(
    'User',{
        'id':fields.Integer(),
        'username':fields.String(required=True, description='username'),
        'email':fields.String(required=True, description='email'),
        'password':fields.String(required=True, description='password'),
        'is_staff':fields.Boolean(description='admin')
    }
)

user_model=auth_namespace.model(
    'User',{
        'id':fields.Integer(),
        'username':fields.String(required=True, description='username'),
        'email':fields.String(required=True, description='email'),
        'password_hash':fields.String(required=True, description='password'),
        'is_active':fields.Boolean(description="User is active or not"),
        'is_staff':fields.Boolean(description="user is staff or not")
    }
)

login_model= auth_namespace.model(
    'Login',{
        'email':fields.String(required=True, description='email'),
        'password':fields.String(required=True, description='password')
    }
)


@auth_namespace.route("/signup")
class SignUp(Resource):
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)
    def post(self):
        """
        Create a new user account (All_users)
        """
        data= request.get_json()
        try:
            new_user=User(
                username=data.get('username'),
                email=data.get('email'),
                password_hash=generate_password_hash(data.get('password')),
                is_staff=data.get('is_staff')
            )
            
            new_user.save()

            return new_user, HTTPStatus.CREATED
        except Exception as e:
            print(e)
            raise Conflict(f"User with email {data.get('email')} exists")


@auth_namespace.route("/login")
class LogIn(Resource):

    @auth_namespace.expect(login_model)
    def post(self):
        """
        Generate a JWT (All_users)
        """
        data= request.get_json()
        email=data.get('email')
        password=data.get('password')

        user= User.query.filter_by(email=email).first()
         # Check if the user exists and the provided password matches the stored hash
        if (user is not None) and check_password_hash(user.password_hash,password): 
            access_token= create_access_token(identity=user.id)
            refresh_token= create_refresh_token(identity=user.id)

            response={
                'access_token':access_token,
                'refresh_token':refresh_token
            }

            return response, HTTPStatus.OK
        
        raise BadRequest("Invalid Username or password")

@auth_namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """
        Refresh the access token using a refresh token (All_users)
        """
        id= get_jwt_identity()
        access_token= create_access_token(identity=id)

        return {"access_token":access_token}, HTTPStatus.OK

@auth_namespace.route('/users')
class UserGet(Resource):
    @auth_namespace.marshal_with(user_model)
    @jwt_required()
    def get(self):
        """
        Get all users (Admin_user)
        """
        current_user_id = get_jwt_identity()  
        user = User.get_by_id(current_user_id)
        if user.is_staff==True:
            users= User.query.all()

            return users, HTTPStatus.OK
        else:
            return "Only staff can see all users", HTTPStatus.OK

    
@auth_namespace.route('/users/<int:user_id>')
class UserUpdateDelete(Resource):
    @auth_namespace.marshal_with(user_model)
    @jwt_required()
    def get(self,user_id):
        """
        Retrive user using id (Admin_user)
        """
        current_user_id = get_jwt_identity()  # Get the current user's identity (user_id)
        user = User.get_by_id(current_user_id)
        if user.is_staff==True:
            user= User.get_by_id(user_id)
            return user, HTTPStatus.OK
        else:
            return "Only staff can access user data", HTTPStatus.OK
        

    @auth_namespace.expect(user_model)
    @auth_namespace.marshal_with(user_model)
    @jwt_required()
    def put(self,user_id):
        """
        update user using id (Admin_user)
        """
        current_user_id = get_jwt_identity()  
        user = User.get_by_id(current_user_id)
        if user.is_staff==True:
            user_to_update= User.get_by_id(user_id)
            data= auth_namespace.payload

            user_to_update.username=data['username']
            user_to_update.email=data['email']
            user_to_update.password_hash=generate_password_hash(data['password_hash'])

            db.session.commit()
            return user_to_update, HTTPStatus.OK
        else:
            return "Only staff can modify user data", HTTPStatus.OK
        

    @auth_namespace.expect(user_model)
    @auth_namespace.marshal_with(user_model)
    @jwt_required()
    def patch(self,user_id):
        """
        Partially update user using id (Admin_user)
        """
        current_user_id = get_jwt_identity()  
        user = User.get_by_id(current_user_id)
        if user.is_staff==True:
            user_to_update = User.get_by_id(user_id)
            data= auth_namespace.payload

            # Update only the fields that are provided in the request
            if 'username' in data:
                user_to_update.title = data['username']
            if 'email' in data:
                user_to_update.director = data['email']
            if 'password_hash' in data:
                user_to_update.rating = generate_password_hash(data['password_hash'])

            db.session.commit()
            return user_to_update, HTTPStatus.OK
        else:
            return "Only staff can modify user data", HTTPStatus.OK
        
    
    @auth_namespace.marshal_with(user_model)
    @jwt_required()
    def delete(self,user_id):
        """
        delete user using id (Admin_user)
        """
        current_user_id = get_jwt_identity()  
        user = User.get_by_id(current_user_id)
        if user.is_staff==True:
            user_to_update= User.get_by_id(user_id)
            user_to_update.delete()

            return user_to_update, HTTPStatus.NO_CONTENT
        else:
            return "Only staff can delete user data", HTTPStatus.OK
        
        
    

       
