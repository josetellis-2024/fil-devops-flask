# GPay API with Flask and Snowflake

A Flask-based REST API that handles bank transactions using Snowflake as the database backend.

## Features

- CRUD operations for bank transactions
- Snowflake database integration
- Docker containerization
- Kubernetes deployment support
- RESTful API endpoints

## Prerequisites

- Python 3.9+
- Docker Desktop
- Minikube
- kubectl
- Snowflake account

## Project Structure

```plaintext
fil-devops-flask/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── routes.py
│   └── utils.py
├── kubernetes/
│   ├── deployment.yaml
│   └── service.yaml
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fil-devops-flask
```

2. Create and activate virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```powershell
pip install -r requirements.txt
```

## Configuration

Update Snowflake credentials in `app/config.py`:
```python
SNOWFLAKE_USER = 'your_username'
SNOWFLAKE_PASSWORD = 'your_password'
SNOWFLAKE_ACCOUNT = 'your_account'
```

## Running Locally

```powershell
# Set Flask environment
$env:FLASK_APP = "app"
$env:FLASK_ENV = "development"

# Run application
flask run
```

## API Endpoints

- GET `/v1/gpay/getall` - Get all transactions
- GET `/v1/gpay/getById/<custId>` - Get transactions by customer ID
- GET `/v1/gpay/getByTransId/<transId>` - Get transaction by transaction ID
- GET `/v1/gpay/getByDate/<from_date>/<to_date>` - Get transactions by date range
- POST `/v1/gpay/transaction` - Create new transaction

## Docker Deployment

```powershell
# Build image
docker build -t gpay-api:latest .

# Run container
docker run -p 5000:5000 gpay-api:latest
```

## Kubernetes Deployment

```powershell
# Start Minikube
minikube start

# Set Docker environment
& minikube -p minikube docker-env | Invoke-Expression

# Build image in Minikube
docker build -t gpay-api:latest .

# Deploy to Kubernetes
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
```

## Testing

Test API endpoints using curl:

```powershell
# Get all transactions
curl http://localhost:5000/v1/gpay/getall

# Create new transaction
curl -X POST http://localhost:5000/v1/gpay/transaction `
-H "Content-Type: application/json" `
-d '{
    "bank_id": "B001",
    "bank_name": "Test Bank",
    "bank_ifs_code": "TESTB0001",
    "cust_id": "C001",
    "cust_name": "John Doe",
    "cust_amt": 1000.00,
    "acct_type": "Savings"
}'
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.