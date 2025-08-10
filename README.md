# SkilledIn

A Django REST Framework–powered AI-First job portal backend that allows companies to post jobs, manage applications, and for candidates to apply for jobs.  
Supports both **full-time** and **internship** job types, with filtering, authentication, and email notifications.

---

## Features

### Authentication & Authorization
- User registration & login (with token authentication)
- Custom user model with roles (e.g., **Hirer** & **Candidate**)
- Role-based permissions

### Job Management
- Create, update, delete job postings
- Separate **full-time** & **internship** jobs with a `job_type` flag
- Filter jobs by type
- View detailed job info
- List jobs posted by a logged-in hirer

### Applications
- Apply to jobs
- View own applications
- Hirers can view all applications for their jobs
- Update application status (shortlisted, rejected, etc.)
- Email applicants

---

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | List all jobs | ❌ |
| GET | `/?job_type=full_time` | List full-time jobs | ❌ |
| GET | `/?job_type=internship` | List internship jobs | ❌ |
| POST | `/create/` | Create a new job posting | ✅ Hirer |
| GET | `/<uuid:id>/` | Job details | ❌ |
| POST | `/apply/` | Apply to a job | ✅ Candidate |
| GET | `/my-applications/` | View user's applications | ✅ Candidate |
| GET | `/my-jobs/` | List jobs posted by current hirer | ✅ Hirer |
| GET | `/<uuid:job_id>/applications/` | View applications for a job | ✅ Hirer |
| PATCH | `/applications/<int:pk>/update-status/` | Update application status | ✅ Hirer |
| POST | `/jobs/<uuid:pk>/email-applicants/` | Email all applicants | ✅ Hirer |

---

## Tech Stack

- **Backend:** Django, Django REST Framework
- **Database:** PostgreSQL (with SSL)
- **Auth:** Token-based Authentication
- **Email:** SMTP (configurable in `.env`)

---

## Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/job-portal-api.git
cd job-portal-api
```

### 2️⃣ Create & Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=defaultdb
DB_USER=avnadmin
DB_PASSWORD=your_password
DB_HOST=your_db_host
DB_PORT=13918
DB_SSLMODE=require

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password
DEFAULT_FROM_EMAIL=your_email@gmail.com
```

**Don't commit `.env` to version control.**

### 5️⃣ Apply Migrations
```bash
python manage.py migrate
```

### 6️⃣ Create Superuser
```bash
python manage.py createsuperuser
```

### 7️⃣ Run the Server
```bash
python manage.py runserver
```

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| SECRET_KEY | Django secret key |
| DEBUG | Debug mode (True/False) |
| ALLOWED_HOSTS | Comma-separated allowed hosts |
| DB_* | PostgreSQL connection details |
| EMAIL_* | SMTP email configuration |

---

## API Testing

You can test the API using:
- [Postman](https://www.postman.com/)
- [HTTPie](https://httpie.io/)
- `curl` commands

Example:
```bash
curl -X GET http://127.0.0.1:8000/?job_type=full_time
```

---

## Security Notes
- Keep your `.env` file private
- Use `DEBUG=False` in production
- Restrict `ALLOWED_HOSTS` to your domain/IP
- Rotate your secret key & DB credentials regularly