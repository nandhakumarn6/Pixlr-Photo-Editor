# Pixlr-Photo-Editor
PIXLR
Django Photo Editor

How To Run The Code

Create Environment 
Virtualenv pixlr-env
Source pixlr-env/bin/activate
Pip install -r  requirement.txt 

-create a DB in postgreSQL
-create a .env file and put
	DB_NAME=DB-name
DB_USER=DB-username
DB_PASS=DB-password
DB_HOST=localhost

Python3 manage.py makemigrations
Python3 manage.py migrate
Python3 manage.py collectstatic --noinput

----RUN THE SERVER!!----
Python3 manage.py runserver

Check localhost:8000


Note: 
●	This is a heroku deployment, cold starting up the servers for the first time may take a while.
●	Consecutive requests will be much faster.
●	Any image uploaded will be removed by heroku after the servers have gone to idle state.
