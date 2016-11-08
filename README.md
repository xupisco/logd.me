# ownCRM

## Screenshot
![Home / Timeline](http://i.imgur.com/JbBo6GL.png)

## Setup

1. Create a virtualenv
2. Run: $pip install -r requirements/dev.txt
3. Create a ```settings.ini``` file with:

```
[settings]  
SECRET_KEY=<anything here>  
DEBUG=True  
DB_ENGINE=django.db.backends.sqlite3  
DB_NAME=conf/db.sqlite3  
```
  
4. $python manage.py migrate
5. $python manage.py createsuperuser
6. $python manage.py runserver
7. Thank @croves...
8. Enjoy!


# Dev drafs

## Models:
    Companies:
        - Name
        - Domain
        - Others?
            - Phone
            - Location
        - Meta
            - Date added
            - Date updates

    People (+ company history):
        - Name
        - E-mail
        - Telefone
        - Role
        - Company
        - Custom fields?
        - Meta
            - Date added
            - Date updates

    Logs:
        - Datetime
        - Type / Title
        - Text
            - @mentions for people or companies
                - Attach (card) to log
        - Tags
        - Meta
            - Date added
            - Date updates

## Views:
    - Timeline
    - Calendar
    - Add / New
    - Search:
        - Contents:
            + Type
            + Text
        - Tags
        - Date
        - People
        - Company


