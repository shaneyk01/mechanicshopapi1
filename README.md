# Mechanic Shop API

Simple Flask REST API to manage customers, mechanics, and service tickets (with many-to-many assignment of mechanics to tickets).

## Features
- Customers CRUD
- Mechanics CRUD
- Service tickets CRUD
- Assign / remove mechanics on a ticket
- Marshmallow serialization
- MySQL (or sqlite if configured) via SQLAlchemy

## Tech Stack
- Python 3.11
- Flask / Flask-SQLAlchemy / Marshmallow
- MySQL (connector) or sqlite fallback

## Requirements
```
python -m pip install -r requirements.txt
```

## Environment
Example config (config/DevelopmentConfig):
- SQLALCHEMY_DATABASE_URI
- SQLALCHEMY_TRACK_MODIFICATIONS = False

## Run
```
# Activate venv (PowerShell)
& venv/Scripts/Activate.ps1
python main.py
```

## Running Workflows

### GitHub Actions Workflows
This repository includes GitHub Actions workflows for continuous integration (CI). The workflows are defined in `.github/workflows/`.

#### Automatic Workflow Execution
Workflows automatically run on:
- **Push events** to `main` or `master` branches

When you push code to these branches, GitHub Actions will:
1. Checkout the code
2. Set up Python 3.12
3. Create a virtual environment
4. Install dependencies from `requirements.txt`
5. Run debugging information
6. Run all tests using unittest

#### View Workflow Runs
1. Go to your repository on GitHub
2. Click on the **Actions** tab
3. View the status of recent workflow runs
4. Click on any run to see detailed logs

#### Manual Workflow Trigger
To manually trigger a workflow:
1. Go to the **Actions** tab on GitHub
2. Select the "Flask CI" workflow
3. Click **Run workflow** button
4. Select the branch you want to run the workflow on
5. Click **Run workflow** to start the workflow

### Running Tests Locally
To simulate the workflow behavior locally:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows PowerShell:
& venv/Scripts/Activate.ps1
# On Windows CMD:
venv\Scripts\activate.bat

# Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Run tests
python -m unittest discover -s test -p "test_*.py"
```

## Database Reset (DEV ONLY)
```
python scripts/reset_db.py
```

## Core Models
- Customer(id, name, email, phone, password, service_tickets[])
- Mechanic(id, name, email, salary, password, service_tickets[])
- ServiceTickets(id, date, customer_id, service_descr, mechanics[])

## API Endpoints (Base: http://127.0.0.1:5000)

### Customers
- POST /customers/
- GET /customers/
- GET /customers/<id>
- PUT /customers/<id>
- DELETE /customers/<id>

### Mechanics
- POST /mechanics/
- GET /mechanics/
- PUT /mechanics/<id>
- DELETE /mechanics/<id>

### Service Tickets
- POST /service_tickets/
- GET /service_tickets/
- PUT /service_tickets/<ticket_id>/add_mechanic/<mechanic_id>
- PUT /service_tickets/<ticket_id>/remove_mechanic/<mechanic_id>

## Example JSON

Create mechanic:
```
{
  "name": "Alice",
  "email": "alice@example.com",
  "salary": 60000,
  "password": "pw"
}
```

Create service ticket:
```
{
  "date": "2025-11-19",
  "customer_id": 1,
  "service_descr": "Brake pad replacement"
}
```

Add mechanic to ticket (PUT):
```
/service_tickets/1/add_mechanic/2
`-

submitted by:shaney hoyohoy

