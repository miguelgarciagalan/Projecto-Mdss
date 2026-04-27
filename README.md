# Proyecto Final MDSS - Cooperativa Olivicola

## Ejecucion con Docker

```bash
docker compose up --build -d
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py popular_db
```

## Ejecucion local (SQLite)

```bash
./venv/bin/python manage.py migrate
./venv/bin/python manage.py createsuperuser
./venv/bin/python manage.py popular_db
./venv/bin/python manage.py runserver
```

## URLs

- `http://localhost:8000` — Dashboard
- `/materia-prima/lotes/` — Lotes de materia prima
- `/produccion/` — Lotes de produccion
- `/admin/` — Administracion
- `/api/swagger/` — Documentacion API
- `/api/token/` — Obtener token JWT


## Env_local

```bash
New-Item .env_local -ItemType File

DEBUG=True
SECRET_KEY=django-insecure-local-key
POSTGRES_DB=oliva_db
POSTGRES_USER=oliva_user
POSTGRES_PASSWORD=oliva_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```


