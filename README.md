# Artisan Platform

Django web platform that connects clients with artisans. Clients post service requests, artisans respond, and both sides can chat and leave reviews. First version, work in progress.

## Features
- Accounts for clients and artisans, with profiles.
- Service categories and service requests.
- Reviews and ratings.
- Notifications and in-app chat between clients and artisans.
- Dashboard.
- Google Maps integration (API key read from the environment).

## Project structure
`apps/` holds one Django app per feature: `accounts`, `artisans`, `clients`, `categories`, `requests`, `reviews`, `notifications`, `chat`, `user_messages`, `dashboard`. Settings are in `config/`, HTML in `templates/`.

## Stack
Python, Django (server-rendered templates), django-crispy-forms, django-phonenumber-field.

## Run locally
```
python -m venv venv
pip install django django-crispy-forms django-phonenumber-field phonenumbers
export SECRET_KEY=change-me
export GOOGLE_MAPS_API_KEY=your-key
python manage.py migrate
python manage.py runserver
```
Secrets are read from environment variables and are not stored in the repository.

## Author
Khalid El Makrini, final-year engineering student, ENSMR (Mines de Rabat).
