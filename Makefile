default: run

DATABASE_NAME=db.sqlite3

configure:
	python configure.py

rebuild: deldb migratedb initdb

deldb:
	rm -f $(DATABASE_NAME)
	rm -rf allauthdemo/auth/migrations/

migratedb:
	python manage.py makemigrations allauthdemo_auth  # important for auth_user table
	python manage.py migrate

initdb:
	sqlite3 $(DATABASE_NAME) < seed.sql

run:
	python manage.py runserver

clean:
	find . -name "*.pyc" -print0 | xargs -0 rm

veryclean: deldb clean
	rm -f allauthdemo/settings_generated.py
