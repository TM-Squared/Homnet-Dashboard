# Dashboard Homnet
## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/10Saavage/Homnet-Dashboard.git
$ cd Homnet-Dashboard
```

Create a virtual environment to install dependencies in and activate it:
```sh
$ python -m venv venv
$ source venv/bin/activate
```

Then install the dependencies:

```sh
(venv)$ python -m pip install -r requirements.txt
```

Once `pip` has finished downloading the dependencies:
```sh
(venv)$ cd homnet-Dashboard
(venv)$ python manage.py makemigrations
(venv)$ python manage.py runserver
```

And navigate to `http://127.0.0.1:8000/`
