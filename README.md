# Flask Todo App – REST API Extension

**Original Repository:** [patrickloeber/flask-todo](https://github.com/patrickloeber/flask-todo)  
**Original Author:** Patrick Loeber  
**Fork Author:** Kit202480087

---

## What Was Added

This fork adds a full **REST API** feature to the original Flask Todo web application on a dedicated branch (`rest-api-feature`).

The original app only supported browser-based interaction through HTML forms. This extension adds proper JSON API endpoints following RESTful principles, making the Todo data accessible to any client (mobile apps, Postman, curl, etc.).

---

## New API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/todos` | Retrieve all todos |
| GET | `/api/todos/<id>` | Retrieve a single todo by ID |
| POST | `/api/todos` | Create a new todo |
| PUT | `/api/todos/<id>` | Update an existing todo |
| DELETE | `/api/todos/<id>` | Delete a todo |

---

## Files Changed / Added

| File | Description |
|------|-------------|
| `api.py` | New file — contains all REST API routes and the SQLAlchemy model |
| `test_api.py` | New file — unit tests with 100% coverage using `unittest` |
| `requirements.txt` | Updated with required packages |

---

## Setup & Installation

1. Clone the repository and switch to the feature branch:
```bash
git clone https://github.com/YOUR_USERNAME/flask-todo.git
cd flask-todo
git checkout rest-api-feature
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the API:
```bash
python api.py
```

---

## Running the Tests

```bash
python -m pytest test_api.py -v
```

---

## Example Requests

**Get all todos:**
```bash
curl http://localhost:5000/api/todos
```

**Create a todo:**
```bash
curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "complete": false}'
```

**Update a todo:**
```bash
curl -X PUT http://localhost:5000/api/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "complete": true}'
```

**Delete a todo:**
```bash
curl -X DELETE http://localhost:5000/api/todos/1
```

---

## HTTP Status Codes Used

| Code | Meaning |
|------|---------|
| 200 | OK – Request succeeded |
| 201 | Created – New todo created |
| 400 | Bad Request – Missing or invalid data |
| 404 | Not Found – Todo does not exist |
