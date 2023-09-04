$env:FLASK_APP="api.__init__:createapp"
flask run

## Get Started

1. Create python virtual environment and activate it.
   ```
    python3 -m venv venv
    ```
2. Install the requirements using requirements.txt
    ```
    pip install -r requirements.txt
    ```

3. To start the flask server run this command.
    ```
    python runserver.py
    ```

## API Endpoints flow:
| METHOD | ROUTE | FUNCTIONALITY | ACCESS |
| --------- | --------- | --------- | --------- |
| *POST* | ```http://127.0.0.1:5000/auth/signup``` | _Register_new_user_ | _All_users_ |
```
Request Body: {
    "username":"admin",
    "email":"admin@gmail.com",
    "password":"admin",
    "is_staff": true   #setting user as an admin
}
```

| METHOD | ROUTE | FUNCTIONALITY | ACCESS |
| --------- | --------- | --------- | --------- |
| *POST* | ```http://127.0.0.1:5000/auth/login``` | _Login_user_ | _All_users_ |
```
Request Body:{
    "email":"admin@gmail.com",
    "password":"admin"
}
```

| METHOD | ROUTE | FUNCTIONALITY | ACCESS |
| --------- | --------- | --------- | --------- |
| *POST* | ```http://127.0.0.1:5000/auth/refresh``` | _refresh_access_token_ | _All_users_ |
```
Headers: Authorization Bearer {token you got in log in }
```

| METHOD | ROUTE | FUNCTIONALITY | ACCESS |
| --------- | --------- | --------- | --------- |
| *POST* | ```http://127.0.0.1:5000/auth/users``` | _get_all_users_ | _All_users_ |
```
Headers: Authorization Bearer {token you got in log in }
```


| METHOD | ROUTE | FUNCTIONALITY | ACCESS |
| --------- | --------- | --------- | --------- |
| *GET* | ```http://127.0.0.1:5000/movies/``` | _List_all_movies_| _All_users_ |


| METHOD | ROUTE | FUNCTIONALITY | ACCESS |
| --------- | --------- | --------- | --------- |
| *POST* | ```http://127.0.0.1:5000/movies/``` | _add_a_movie_| _Admin_user_ |
```
Headers: Authorization Bearer {token you got in log in }
Body: {
    "title": "Bro",
    "director": "Samuthirakani",
    "rating": "7.1",
    "year": 2023,
    "genre": "Drama",
    "description": "A Fantastic movie"
}
```

| METHOD | ROUTE | FUNCTIONALITY | ACCESS |
| --------- | --------- | --------- | --------- |
| *GET* | ```http://127.0.0.1:5000/movies/id``` | _get_a_movie_by_id_ | _All_users_ |


| METHOD | ROUTE | FUNCTIONALITY | ACCESS |
| --------- | --------- | --------- | --------- |
| *PUT* | ```http://127.0.0.1:5000/movies/id``` | _update_a_movie_by_id| _Admin_user_ |
```
Headers: Authorization Bearer {token you got in log in }
Body: {
    "title": "Bro",
    "director": "Samuthirakani",
    "rating": "7.1",
    "year": 2020,
    "genre": "Action",
    "description": "A Fantastic movie"
}
```

| METHOD | ROUTE | FUNCTIONALITY | ACCESS |
| --------- | --------- | --------- | --------- |
| *PATCH* | ```http://127.0.0.1:5000/movies/id``` | _partially_update_a_movie_by_id_| _Admin_user_ |
```
Headers: Authorization Bearer {token you got in log in }
Body: {
    "year": 2023,
    "genre": "Drama",
}
```

| METHOD | ROUTE | FUNCTIONALITY | ACCESS |
| --------- | --------- | --------- | --------- |
| *DELETE* | ```http://127.0.0.1:5000/movies/id``` | _delete_a_movie_by_id_| _Admin_user_ |
```
Headers: Authorization Bearer {token you got in log in }
```

Similarly the above put, patch and delete methods can be used on users as well with the url path to auth/id.


| METHOD | ROUTE | FUNCTIONALITY | ACCESS |
| --------- | --------- | --------- | --------- |
| *POST* | ```http://127.0.0.1:5000/movies/search``` | _movies_robust_search_| _All_users_ |
```
Body:{
    "year": 2007,
    "genre":"Fantasy"
}
```