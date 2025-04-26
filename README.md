# goit-pythonweb-hw-06

 Студентська база даних.

Використано:
- PostgreSQL (у Docker)
- SQLAlchemy
- Alembic
- Faker

## Запуск

1. Запустити PostgreSQL:

docker run --name students-db -p 5432:5432 -e POSTGRES_PASSWORD=12345 -d postgres

2. Створити базу:

docker exec -it students-db psql -U postgres

CREATE DATABASE students;
\q

3. Застосувати міграції:

alembic upgrade head

4. Наповнити даними:

python src/seed.py

## Виконання запитів:

python src/main.py -q 1

## CRUD приклади:

python src/crud_cli.py -a create -m Teacher -n "John Doe"


