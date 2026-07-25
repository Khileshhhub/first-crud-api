# FastAPI CRUD API with PostgreSQL

## Overview

A REST API built with FastAPI and PostgreSQL. The application is fully containerized using Docker Compose and supports complete CRUD operations for tasks.

## Tech Stack

- FastAPI
- PostgreSQL
- Psycopg
- Docker
- Docker Compose
- Python 3.12

---

## Run the Project

Clone the repository:

```bash
git clone <YOUR_REPOSITORY_URL>
cd first-crud-api
```

Copy the environment file:

```bash
cp .env.example .env
```

Start everything:

```bash
docker compose up
```

The API will be available at:

```
http://localhost:3000
```

Swagger UI:

```
http://localhost:3000/docs
```

---

## Environment Variables

Create a `.env` file using `.env.example`.

Example:

```env
DATABASE_URL=postgres://postgres:dev@db:5432/tasks
```

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | / | API information |
| GET | /health | Health check |
| GET | /tasks | List all tasks |
| GET | /tasks/{id} | Get one task |
| POST | /tasks | Create task |
| PUT | /tasks/{id} | Update task |
| DELETE | /tasks/{id} | Delete task |

---

## Example curl

```bash
curl -i -X POST http://localhost:3000/tasks \
-H "Content-Type: application/json" \
-d "{\"title\":\"Learn Docker\"}"
```

Example response:

```
HTTP/1.1 201 Created

{
  "id": 1,
  "title": "Learn Docker",
  "done": false
}
```

---

## Database Screenshot

Add a screenshot showing:

- `\dt`
- `SELECT * FROM tasks;`

or a screenshot from DBeaver, pgAdmin, or TablePlus.

---

## Docker

Start:

```bash
docker compose up
```

Stop:

```bash
docker compose down
```
