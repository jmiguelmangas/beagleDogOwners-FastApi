# Beagle Dog Owners API - FastAPI

This project is an API built with FastAPI to manage information about Beagle dog owners and their dogs. It allows users to perform various CRUD (Create, Read, Update, Delete) operations on dog and owner records, and also supports searching by city, name, and more.

## Features

- Manage owners (create, read, update, delete)
- Manage dogs (create, read, update, delete)
- Search for owners by name and surname
- Search for dogs by owner or city
- Calculate dog’s age based on birth date
- Pagination for efficient data retrieval

## Technologies

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+.
- **SQLAlchemy**: For SQL database ORM (Object Relational Mapper).
- **SQLite**: The database used in the project.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **Uvicorn**: ASGI server for serving the FastAPI app.

## Setup Instructions

### Prerequisites

- Python 3.8+
- `pip` installed

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/jmiguelmangas/beagleDogOwners-FastApi.git
   cd beagleDogOwners-FastApi

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt

4. Set up the database: Run the following script to create the database and the tables.
    ```bash
    python database.py

5. Running the API

Start the FastAPI server:

uvicorn main:app --reload

Open your browser and go to the interactive API documentation:

Swagger UI
ReDoc

Testing with Postman
You can test the API endpoints using Postman or any other API client. The base URL is:


http://127.0.0.1:8000

# Example Endpoints
Create an owner: POST /owners/

Sample payload:

json

{
  "nombre": "Alicia",
  "apellidos": "Smith",
  "city": "New York",
  "postalcode": 10001,
  "email": "alicia.smith@example.com",
  "telefono": "+123456789"
}
# Create a dog: POST /dogs/



json
{
  "nombre_perro": "Buddy",
  "fecha_nacimiento": "2019-05-14",
  "peso": 12.5,
  "owner_id": 1,
  "sexo": "male",
  "esterilizado": true
}

Search for owners by name and surname: GET /owners/search?nombre=Alicia&apellidos=Smith

Search for dogs by city: GET /dogs/search?city=New York

# Folder Structure

graphql
├── main.py          # The main FastAPI application
├── database.py      # SQLAlchemy models and database setup
├── models.py        # Models for owners and dogs
├── schemas.py       # Pydantic schemas for validation
├── requirements.txt # Project dependencies
└── README.md        # Project documentation
## Contributing
Feel free to fork this repository and make improvements. Pull requests are welcome!

## License
This project is licensed under the MIT License.