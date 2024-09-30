echo 'Building the project...'
pip install setuptools
pip -m pip install -r requirements.txt


# Run Django migrations (optional but recommended)
echo 'Make Migrations'
python manage.py make migrations --noinput
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput --clear