#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate
python manage.py create_initial_categories

echo "Collecting static files..."
python manage.py collectstatic --noinput


python manage.py shell <<EOF
from django.contrib.auth import get_user_model

User = get_user_model()
username = 'admin'
email = 'admin@admin.com'
password = 'admin'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)

# Creating categories...
categories_to_create = ['Tech', 'Life', 'Music', 'Nature', 'Cars']
    
for name in categories_to_create:
    if not Category.objects.filter(name=name).exists():
        Category.objects.create(
            name=name,
            slug=slugify(name) 
        )

EOF
echo "Starting server..."
exec "$@"
