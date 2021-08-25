# Just Another Journal App 📝✨

It's just another journal app but a highly customized one, ad-free and loads faster than free blog sites. The web app is built with Python and Django Frameworok (my current favourite). The goal is not to reinvent the wheel but to learn in the process of building from scratch and having a content management system that suits my interest and caters to my study requirements.

## Instructions
1. Clone repository
2. `python manage.py makemigrations` & `python manage.py migrate` to restart SQLite
3. `python manage.py createsuperuser` to create an administrator account
4. `python manage.py runserver` -- You might come across a few errors because of the editable fields. The `field_id` must match the query in `blog/views.py`
