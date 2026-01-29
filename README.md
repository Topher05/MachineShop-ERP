# MachineShop-ERP

MachineShop ERP is a specialized Enterprise Resource Planning (ERP) system designed for machine shops.  
It automates quoting, production tracking, and AS9102 quality workflows while maintaining full traceability and compliance.

---

### Prerequisites
- Docker Desktop (Windows/macOS) or Docker Engine (Linux)
- Git

### Start the Application

From the project root directory:

```bash
docker-compose up --build -d
```

### Create an Admin User

```bash
docker-compose exec web python manage.py createsuperuser
```

### Access the Application

**Admin Dashboard:** http://localhost:8000/admin

---

### (Optional) Initialize the Database and Load Demo Data

Once the containers are running:

```bash
# Create database tables
docker-compose exec web python manage.py migrate

# Load demo data (Customers, Quotes, Jobs, Inspections)
docker-compose exec web python manage.py load_demo_data
```

## Manual Installation (Without Docker)

Use this method if you prefer to run Python directly on your local machine.

### Prerequisites
- Python 3.11 or newer
- Git

### Create and Activate a Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Initialize the Database and Demo Data

```bash
python manage.py migrate
python manage.py load_demo_data
```

### Create Admin User and Run the Server

```bash
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

### Access the Application

**Admin Dashboard:** http://localhost:8000/admin

---

## License

License information to be added.

---

## Summary

MachineShop ERP is built for machine shops that require precision, traceability, and compliance across quoting, production, and quality operations.
