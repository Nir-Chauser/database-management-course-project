# TODO: Review this README before publishing

# Student Project B

This repository contains a Django-based rental management and query project. It includes a web application, SQL assets, CSV data files, and supporting coursework materials.

## Tech Stack

- Python
- Django
- HTML templates
- CSS
- SQL Server configuration

## Project Structure

```text
student_project_b/
├── manage.py
├── student_project_b/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── Rentals_App/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
├── templates/
├── static/
├── data/
└── queries_views.sql
```

## Setup

Create and activate a virtual environment, then install the project dependencies you need.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install django pyodbc mssql-django
```

## Running the Project

Update the database settings if needed, then run:

```bash
python manage.py runserver
```

## Notes

- The project currently uses SQL Server settings in `settings.py`.
- The repository still includes coursework reference files and sample data.
- Review which PDFs and zip files should remain in a public repository.

## What Still Needs Review

- Replace or externalize any non-public database settings if this will be published.
- Review whether duplicate submission artifacts should stay in the repository.
- Check data files for any real-world sensitive information before publishing.
