rm -r luke/migrations
python3 manage.py makemigrations luke
python3 manage.py migrate
