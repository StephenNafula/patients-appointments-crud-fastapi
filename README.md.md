#  Patients & Appointments CRUD API (FastAPI) — Single File Version

This is a minimal **single-file FastAPI application** that provides CRUD operations for **Patients** and their **Appointments** using SQLite and SQLAlchemy.

---

##  Installation & Setup

###  Clone the repository or copy the `main.py` file

###  Create a virtual environment
```bash
python -m venv venv
# Activate it
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

###  Install dependencies
```bash
pip install -r requirements.txt
```

###  Run the application
```bash
uvicorn main:app --reload
```

The app will start at: **http://127.0.0.1:8000**

- Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

##  API Endpoints

###  Patients
- `POST /patients/` → Create a patient
- `GET /patients/` → List all patients
- `GET /patients/{id}` → Get patient by ID
- `PUT /patients/{id}` → Update patient
- `DELETE /patients/{id}` → Delete patient

###  Appointments
- `POST /appointments/` → Create an appointment
- `GET /appointments/` → List all appointments
- `GET /appointments/{id}` → Get appointment by ID
- `PUT /appointments/{id}` → Update appointment
- `DELETE /appointments/{id}` → Delete appointment

---

##  Example Requests (cURL)

Create a patient:
```bash
curl -X POST "http://127.0.0.1:8000/patients/" \
     -H "Content-Type: application/json" \
     -d '{"name": "John Doe", "age": 30, "gender": "Male"}'
```

Create an appointment:
```bash
curl -X POST "http://127.0.0.1:8000/appointments/" \
     -H "Content-Type: application/json" \
     -d '{"patient_id": 1, "date": "2025-09-25T10:00:00", "reason": "Routine checkup"}'
```

---

##  Project Files
```
main.py             # FastAPI single-file app
requirements.txt    # Dependencies
README.md           # Documentation
```

---


