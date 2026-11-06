web: python manage.py migrate && python manage.py collectstatic --noinput && python scripts/seed_all.py && gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8000}

