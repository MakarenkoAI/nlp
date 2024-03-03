To run project:
```sh
python manage.py runserver
```

If you don't have django installed, try:
```sh
pip install pipenv
cd project
pipenv install django==3.0.*
pipenv shell
python manage.py migrate
python manage.py runserver
```

To see how create a django project [click](https://python-scripts.com/django-manage-py-startapp?ysclid=ltae1zm3fi162955961) or use commands below:
```sh
 django-admin startproject project .
 python manage.py migrate
 python manage.py runserver

 python manage.py startapp pages
```