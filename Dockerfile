# used the same python version for development environment
FROM python:3.10.12

LABEL authors="aashishnk"

# Set environment variables for the container:
# .pyc will not be generated(is a form of caching to improve performance)
ENV PYTHONDONTWRITEBYTECODE 1
# python output(stdout+stderr) are sent directly to the terminal and not buffered/stored anywhere
ENV PYTHONUNBUFFERED 1


# set the working directry in the container
WORKDIR /app

# install mysql client
RUN apt-get update && apt-get install -y default-mysql-client && rm -rf /var/lib/apt/lists/*

# copy the current directory into /app
COPY . /app/

# install the required packages from requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# expose the port the app runs on
EXPOSE 8000

# run migrate and then start the Django dev server
CMD ["python manage.py wait_for_db && python manage.py wait_for_redis && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]