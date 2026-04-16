# 💼 Jobs Portal (Django + Docker + PostgreSQL)

A full-stack job portal built with Django, containerized using Docker, and integrated with PostgreSQL.  
The project includes CI/CD pipelines using GitHub Actions with staging and production workflows.

---

## 🚀 Features

- User authentication (customizable)
- Job listing system
- Job applications management
- PostgreSQL database integration
- Dockerized development environment
- CI pipeline using GitHub Actions
- Staging & production branch workflow
- Ready for cloud deployment

---

## 🏗️ Tech Stack

- **Backend:** Django (Python)
- **Database:** PostgreSQL
- **Containerization:** Docker, Docker Compose
- **CI/CD:** GitHub Actions
- **Version Control:** Git & GitHub

---

## 📁 Project Structure



---

## ⚙️ Setup Instructions

### 1. Clone the repository

git clone git@github.com:your-username/python-jobs-portal.git
cd python-jobs-portal

### 2. Create .env File

DB_NAME=jobsdb
DB_USER=jobsuser
DB_PASSWORD=jobspass
DB_HOST=db
DB_PORT=5432

DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True

### 3. Build and run with Docker

docker compose up --build

### 4. Run migrations

docker compose exec web python manage.py migrate

### 5. Create superuser

docker compose exec web python manage.py createsuperuser

### 6. Access the app

Web app: http://127.0.0.1:8000
Admin panel: http://127.0.0.1:8000/admin
