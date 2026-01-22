# Telegram Bot AI

## Migrations with Alembic
```bash
# Initialize the database
alembic upgrade head

# Apply migrations
alembic upgrade head

# Rollback migrations
alembic downgrade -1

# Rollback all migrations
alembic downgrade base

# Create a new migration
alembic revision --autogenerate -m "Add new table"

# Edit an existing migration
alembic revision --autogenerate -m "Edit existing table"
```
