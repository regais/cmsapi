# BlogPostAPI Project

## Requirements

### python3

```
sudo apt install python3 python3-setuptools
```

### django and rest framework

```
pip3 install django
pip3 install djangorestframework
```

## Initialize project

```
python3 manage.py migrate
python3 manage.py createsuperuser --email admin@test.com --username admin
```

## Run API server on all Server IPs on port 8080

```
python manage.py runserver 0.0.0.0:8080
```

