#!/bin/bash

# Migrate the database
python manage.py makemigrations
python manage.py migrate