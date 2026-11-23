# Ridebox

Web app for **Ridebox**, a startup-competition product: a pedal-powered energy storage kit (LiFePO4 battery) for homes and small businesses.

## Features
- Home page with a first-visit language popup
- Product catalog loaded from a SQLite database
- Login and an admin dashboard to add/delete products

## Tech
Python, Flask, Flask-SQLAlchemy (SQLite), Bootstrap 5, Docker

## Run locally
```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000 — demo login: `admin` / `admin123`

## Run with Docker
```bash
docker build -t ridebox .
docker run -p 5000:5000 ridebox
```
