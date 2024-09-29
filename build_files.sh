pip install -r requirements.txt

# Run Django migrations (optional but recommended)
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput