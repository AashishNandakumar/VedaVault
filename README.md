# Ramayan book store

> APIs available for this project
![Screenshot 2024-03-03 at 15-00-03 SF Webmasters API](https://github.com/AashishNandakumar/SF-backend/assets/98106129/031e661a-28d1-48fb-813e-74f8cbb7e804)


> Built in Django

## Getting Started

These instructions will get your copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.x
- pip (Python package manager)

### Clone the Project
After creating the venv in the root directory execute the following command:
```bash
git clone https://github.com/AashishNandakumar/SF-backend.git
```

### Setting Up a Virtual Environment

It's recommended to use a virtual environment for Python projects. This keeps dependencies required by different projects separate by creating isolated environments for them.

To create a virtual environment, navigate to your project directory in the terminal and run:

```bash
python3 -m venv venv
```
This command will create a virtual environment named `venv` in your project directory.

### Activating the Virtual Environment
Before installing the dependencies, you need to activate the virtual environment.

On macOS and Linux:
```bash
source venv/bin/activate
```

On windows:
```bash
.\venv\Scripts\activate
```

### Installing Dependencies
With the virtual environment activated, install the project dependencies by running:
```bash
pip install -r requirements.txt
```
This command reads the `requirements.txt` file in your project directory and installs all the necessary packages listed there.

### Applying Migrations
Django uses migrations to propagate changes made to models (adding a field, deleting a model, etc.) into the database schema. Run the following commands to apply migrations:
```
python manage.py makemigrations
python manage.py migrate
```

### Creating a Superuser
To access the Django admin, you'll need to create a superuser account in the database. Run the following command and follow the prompts:
```bash
python manage.py createsuperuser
```

### Fill the required credentials in .env
```bash
USER1='mysql_user'
PASSWORD1='mysql_pwd'
BUCKET_NAME='s3_bucket_name'
REGION='aws_region'
AWS_ACCESS_KEY_ID = 'aws_access_key_id'
AWS_SECRET_ACCESS_KEY = 'aws_secret_access_key'
AWS_REGION = 'aws_region'
```

### Running the development server
To start the Django development server, run:
```bash
python manage.py runserver
```
This will start the server on `http://127.0.0.1:8000/` by default. You can access the application by visiting this URL in your web browser.
