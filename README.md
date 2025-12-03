# Flight Routes System (Django)

Small Django app for the Machine Test. Implements:

- Add Airport Route (airport code, position, duration)
- Search Nth left/right node from a given airport
- Display longest node (by duration)
- Display shortest node between two airports (by position range)

Quick start

1. Create a virtual environment and activate it.
2. Install dependencies: pip install -r requirements.txt
3. Run migrations: python manage.py migrate
4. Create a superuser (optional): python manage.py createsuperuser
5. Run the server: python manage.py runserver

Open http://127.0.0.1:8000/ to use the app.

Notes

Assumptions made:
- Routes are ordered by the integer "position" field.
- "Left" means lower position values; "Right" means higher position values.
- "Between two airports" searches the interval of positions between the two airport codes (inclusive) and finds the minimum duration in that slice.

Publishing to GitHub

1. Initialize a git repo and commit the project (if not already):

	git init
	git add .
	git commit -m "Initial commit - Flight Routes System"

2. Create a repository on GitHub and follow the instructions to push:

	git remote add origin https://github.com/<your-username>/<repo-name>.git
	git branch -M main
	git push -u origin main

Notes:
- The `requirements.txt` file is pinned to the versions used during development. When developers clone the repo, they should create and activate a virtual environment and run `pip install -r requirements.txt`.
- The `.gitignore` excludes `venv/`, local SQLite DB and compiled files.

