echo 'Building the project...'
python3.12 install setuptools
python3.12 install -r requirements.txt


# Run Django migrations (optional but recommended)
echo 'Make Migrations'
python3.12 manage.py make migrations --noinput
python3.12 manage.py migrate

# Collect static files
python3.12 manage.py collectstatic --noinput --clear