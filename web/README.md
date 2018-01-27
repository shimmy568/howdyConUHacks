# FLASK-BACKEND

### WHAT THIS DOES
* database
* login / register / basic http auth
* example of scheduled tasks
* return HTML example

### DEPENDENCIES
* flask
* flask_restful
* flask_sqlalchemy
* flask_httpauth
* itsdangerous

### RUN
```
python3 api.py
```

### TEST
#### REGISTER
```
curl -H "Content-Type: application/json" -X POST -d '{"username":"user","password":"password"}' http://127.0.0.1:5000/register
```
#### LOGIN
```
curl --user user:password http://127.0.0.1:5000/register
```

### INIT DB
```
python3
>>> from api import init_db
>>> init_db()
init db
```