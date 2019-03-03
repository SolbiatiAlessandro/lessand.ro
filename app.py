"""
so this short module is to fix the integration problems with heroku and flask: I was trying to put in the gunicorn flaskr:create_app and I was getting a TypeError, I am trying to write a solution as mentioned here

https://stackoverflow.com/questions/51395936/how-to-get-flak-app-running-with-gunicorn

all this problem arise because my app is not in a single module but is actually in the folder flaskr, as explained in flask tutorial

"Instead of creating a Flask instance globally, you will create it inside a function. This function is known as the application factory. Any configuration, registration, and other setup the application needs will happen inside the function, then the application will be returned."

so inside __init__.py there is a create_app() method that will be called here to get a callable instance of the FLASK app to give to WSGI, you can test that the previous sentence is true if you put yourself in this directory and on the python REPL write 

>>> from lessandro import create_app;create_app()
<Flask 'flaskr'>
"""
from lessandro import create_app

if __name__ == "__main__":
    # this is to be run as python app.py
    app = create_app()
    app.run()
else:
    # this is to be run by gunicorn
    gunicorn_app = create_app()
