# Mentoria

Level-based online learning platform for Uzbekistan: course marketplace, tutor finder, mentorship and free open lectures.
Graduation project GP-26-SE-D-03, New Uzbekistan University. See [CLAUDE.md](CLAUDE.md) for the full project guide.

## Setup (Windows, PowerShell)

Requires Docker Desktop. The backend runs **only in Docker** (Python 3.12 image).

```powershell
Copy-Item .env.example .env        # then edit values if needed
docker compose up --build          # db + backend (:8000) + frontend (:5173)
```

- API health check: http://localhost:8000/api/v1/health/
- Frontend: http://localhost:5173
- Django admin: http://localhost:8000/admin/

## Common commands

```powershell
docker compose run --rm backend pytest --cov=apps          # backend tests
docker compose run --rm backend python manage.py makemigrations
docker compose run --rm backend python manage.py createsuperuser
```

Frontend can also run locally with Node 24: `cd frontend; npm install; npm run dev`.

## Git workflow

Small commits (`feat:`, `fix:`, `test:`, `docs:`, `chore:`), feature branches, merge through pull requests. CI runs the backend tests on every push and PR.
