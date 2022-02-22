# Flask TODO App

## Want to use this project?

### Basics

1. Fork/Clone
2. Activate a virtualenv
3. Install the requirements

### Set a flask secret key:

Update *app/config.py*

SECRET_KEY="change_me"

### Create DB

Create the database in `SQLite`:

```sh
$ sqlite database.db
# .quit
```

Create the tables:
```sh
$ python manage.py create_db
```

### Run the Application

```sh
$ python manage.py runserver
```

Access the application at the address [http://localhost:5000/](http://localhost:5000)

> Want to specify a different port?
> ```sh
> $ python manage.py runserver -h 0.0.0.0 -p 8080
> ```