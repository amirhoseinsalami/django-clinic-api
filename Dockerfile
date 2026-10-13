#start with python image
FROM python:3.12

# Inside container: /app becomes project folder.
WORKDIR /app


COPY requirements.txt .

RUN pip install -r requirements.txt

# Move your code into container.
COPY . .

# Command when container starts. Equivalent: python manage.py runserver
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]   # it is for development

# it is for production
# means : config/wsgi.py, find application and run it
# --bind 0.0.0.0:8000 means Listen on all network interfaces.
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"] 