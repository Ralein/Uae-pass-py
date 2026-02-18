# UAE Digital Identity Platform - Backend

## Setup

1.  **Install Poetry**:
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

2.  **Install Dependencies**:
    ```bash
    cd backend
    poetry install
    ```

3.  **Environment Variables**:
    Copy `.env.example` to `.env`:
    ```bash
    cp .env.example .env
    ```

4.  **Start Services (DB + Redis)**:
    ```bash
    docker-compose up -d
    ```

5.  **Run Migrations**:
    ```bash
    poetry run alembic upgrade head
    ```

6.  **Run Application**:
    ```bash
    poetry run uvicorn app.main:app --reload
    ```

## Testing

Run tests with pytest:
```bash
poetry run pytest
```

## Pre-commit

Install hooks:
```bash
poetry run pre-commit install
```
