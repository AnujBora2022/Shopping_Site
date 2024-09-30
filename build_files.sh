echo 'Building the project...'
python3.12 install setuptools
python3.12 install -r requirements.txt


# Run Django migrations (optional but recommended)
echo 'Make Migrations'
python manage.py make migrations --noinput
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput --clear