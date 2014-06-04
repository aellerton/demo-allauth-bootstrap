default: run

DATABASE_NAME=db.sqlite3

rebuild: deldb syncdb initdb

deldb:
	rm -f $(DATABASE_NAME)

syncdb:
	python manage.py syncdb --noinput

# Generate seed.sql by running "python configure.py"
initdb:
	sqlite3 $(DATABASE_NAME) < seed.sql

run:
	python manage.py runserver

clean:
	find . -name "*.pyc" | xargs rm
