For this app to work you need to initialize db for users first
we are using flask-migrate.
In your project folder execute 
pip install -r requirements.txt && flask db init && flask db migrate -m "Initial migration." && flask db upgrade

