# Database Management Course Project

This repository contains a course project developed for the Database Management course at the Technion - Israel Institute of Technology.

The project focuses on a rental-apartment database system and combines relational data, SQL queries and views, and a Django-based application layer for presenting and analyzing the data.

## Authors

- Nir
- Sagi

## Semester

Spring 2025

## Project Overview

The system manages information about:

- apartment owners
- apartments
- rental records

The project includes:

- Django models mapped to the database tables
- SQL queries and views for analysis tasks
- pages for displaying query results
- forms for adding rental records
- search and analysis tools for owners and apartments

## Repository Contents

- `Rentals_App/` - main Django application code
- `templates/` - HTML templates
- `static/` - static assets
- `data/` - CSV data files and SQL setup scripts
- `manage.py` - Django management entry point
- `queries_views.sql` - SQL queries and database views used in the project

## Running the Project

This repository contains the main application files and data used in the project.

To run it locally, you need:

1. Python and Django installed
2. a configured database with the project tables and views
3. local Django project settings available for `manage.py`

Typical steps:

1. Load the database data and setup scripts from `data/`
2. apply the SQL definitions from `queries_views.sql`
3. make sure the Django settings and database connection are configured locally
4. run the Django server with:

```bash
python manage.py runserver
```

## Institution

Technion - Israel Institute of Technology
