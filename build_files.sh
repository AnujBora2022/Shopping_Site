echo 'Building the project...'
python3.9 -m pip install -r requirements.txt

# Run Django migrations (optional but recommended)
echo 'Make Migrations'
python3.9 manage.py make migrations --noinput
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput --clear