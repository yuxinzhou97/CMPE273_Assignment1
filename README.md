# CMPE273_Assignment1

Requirements:
https://github.com/sithu/cmpe273-fall20/tree/master/assignment1

## Install Dependencies

```
pipenv install Flask==1.1.1
pipenv install pillow qrcode
pipenv install flask_monitoringdashboard
pipenv install sqlitedict
pipenv install flask-restful
pipenv install shortuuid
pipenv install qrcode
pipenv install git+git://github.com/ojii/pymaging.git#egg=pymaging
pipenv install git+git://github.com/ojii/pymaging-png.git#egg=pymaging-png
```

## Run Server

```
pipenv shell
export FLASK_APP=app.py
flask run
```
