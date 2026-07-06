# Flask & PostgreSQL Items API

This is a lightweight Python Flask application that provides a RESTful API to manage an inventory of items stored in a PostgreSQL database. It is designed to run in containerized environments (either locally using Docker Compose or on a Kubernetes cluster).

---

## Directory Structure

```
flask/
├── app/
│   ├── app.py              # Flask application logic & routing
│   ├── Dockerfile          # Container definition for the Flask app
│   └── requirements.txt    # Python package dependencies
├── k8s/                    # Kubernetes manifests (deployments, services, ingress, monitoring)
│   └── README.md           # K8s deployment instructions
├── docker-compose.yml      # Local multi-container development configuration
├── init.sql                # SQL script to initialize the PostgreSQL schema
├── .gitignore              # Files ignored by version control
└── README.md               # This file
```

---

## Configuration (Environment Variables)

The application dynamically configures its database connection using the following environment variables:

| Variable | Description | Default (Local/Compose) |
| :--- | :--- | :--- |
| `DB_HOST` | Hostname of the PostgreSQL server | `db` |
| `DB_PORT` | Port of the PostgreSQL server | `5432` |
| `DB_NAME` | Database name | `appdb` |
| `DB_USER` | Database user name | `appuser` |
| `DB_PASSWORD`| Database user password | `apppassword` |

---

## Database Schema

During initialization, the database runs `init.sql` to create the following table:

### `items` Table
* `id` (SERIAL, Primary Key)
* `name` (VARCHAR(255), Not Null)
* `quantity` (INTEGER, Default 0)
* `created_at` (TIMESTAMP, Default `NOW()`)

---

## API Endpoints

### 1. Health Check
* **Endpoint**: `GET /health`
* **Description**: Verifies API availability and validates connection health to the PostgreSQL database.
* **Success Response (200 OK)**:
  ```json
  {
    "status": "ok",
    "db": "connected"
  }
  ```
* **Error Response (503 Service Unavailable)**:
  ```json
  {
    "status": "error",
    "db": "connection error message details"
  }
  ```

### 2. List All Items
* **Endpoint**: `GET /items`
* **Description**: Retrieves all items stored in the inventory, ordered by ID.
* **Success Response (200 OK)**:
  ```json
  [
    {
      "id": 1,
      "name": "Sample Widget",
      "quantity": 42,
      "created_at": "Mon, 06 Jul 2026 05:00:00 GMT"
    }
  ]
  ```

### 3. Create Item
* **Endpoint**: `POST /items`
* **Description**: Adds a new item to the inventory.
* **Request Payload**:
  ```json
  {
    "name": "Super Widget",
    "quantity": 10
  }
  ```
* **Success Response (201 Created)**:
  ```json
  {
    "id": 2,
    "name": "Super Widget",
    "quantity": 10,
    "created_at": "Mon, 06 Jul 2026 05:05:00 GMT"
  }
  ```

### 4. Delete Item
* **Endpoint**: `DELETE /items/<item_id>`
* **Description**: Removes an item from the inventory.
* **Success Response (204 No Content)**: *(No body)*
* **Error Response (404 Not Found)**:
  ```json
  {
    "error": "item not found"
  }
  ```

---

## Local Development (Docker Compose)

To launch the entire stack (Flask app + PostgreSQL database) locally:

1. Build and run the containers:
   ```bash
   docker-compose up --build
   ```
2. The Flask API will be accessible on `http://localhost:5000`.
3. Try listing the initialized data:
   ```bash
   curl http://localhost:5000/items
   ```
4. Stop the services:
   ```bash
   docker-compose down
   ```

---

## Production & Staging Deployment (Kubernetes)

To deploy the application to a Kubernetes cluster (e.g., our Kind-on-a-Box cluster), see the step-by-step instructions inside the [k8s/README.md](k8s/README.md) file.
