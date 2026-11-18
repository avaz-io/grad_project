# Mentoria — Project Guide for Claude Code

Graduation project **GP-26-SE-D-03**, School of Computing, New Uzbekistan University (BSc Software Engineering, D-Type / development project).
Team: Soibnazarov Avazbek (230047), Mamatov Shohruh (230048), Abdurazzoqov Abdurahmon (230045). Supervisor: Assadullah Tariq.

## What we are building

**Mentoria** is a level-based online learning web platform for learners in Uzbekistan. It has four parts:

1. **Course marketplace**: educators create, price and publish self-paced courses (video, PDF, quiz lessons). Students search and filter by subject, level, language and price, enrol, pay (test mode) and track progress.
2. **Tutor finder**: tutors publish profiles (subjects, levels, hourly rate, languages, weekly availability). Students see a ranked list, book a lesson slot, and leave ratings and reviews.
3. **Mentorship**: mentors publish their free time for one-to-one advice and consulting sessions (career, study planning, university applications). Sessions can be free or paid. Tutors and mentors share the same booking engine.
4. **Free open lectures**: a public library of recorded lectures plus scheduled live lectures with registration. Anyone can open these, no payment needed.

Cross-cutting features:
- **Placement test**: a short rule-based adaptive test per subject. The next question gets harder after a correct answer and easier after a wrong one. The final score maps to a level (Beginner / Intermediate / Advanced; CEFR A1–C2 for English). The level drives course recommendations and tutor ranking.
- **Tutor matching**: a transparent weighted score (level fit, budget fit, schedule overlap, language, Bayesian-smoothed rating). No ML.
- **Zoom integration**: when a tutoring or mentoring session is confirmed, or a live lecture is scheduled, the backend creates a Zoom meeting through the Zoom Meeting API (Server-to-Server OAuth) and stores the join link.
- **Roles**: `student`, `educator`, `tutor`, `mentor`, `admin` (role-based permissions on every endpoint).
- **Admin panel**: approve courses, verify tutors and mentors, handle reports (use Django admin where possible).
- **Interface languages**: English and Uzbek.

Out of scope: our own video-calling system, native mobile apps, real-money payouts, ML recommendation models, live chat.

## Tech stack (keep it minimal)

The supervisor asked us to use as few tools as possible. **Do not add new frameworks, services or libraries beyond this list without asking first.**

| Area | Tool |
|---|---|
| Languages | Python 3.12, TypeScript |
| Backend | Django 5.x + Django REST Framework |
| Frontend | React 18+ with TypeScript (Vite only as the build tool) |
| Database | PostgreSQL 16 |
| Integrations | Zoom Meeting API, Stripe (test mode) |
| Testing | PyTest (with pytest-django) |
| Version control, tasks, CI | GitHub (repo, Projects board, GitHub Actions) |
| Design | Figma (outside the repo) |
| Deployment | Docker + Docker Compose, DigitalOcean server |
| Editor | VS Code |

Allowed small libraries: `djangorestframework-simplejwt` (JWT auth), `django-cors-headers`, `psycopg` (PostgreSQL driver), `python-dotenv` or `django-environ` (env vars, pick one), `pytest`, `pytest-django`, `pytest-cov`, `react-router-dom`. For HTTP calls in the frontend use the built-in `fetch`. For UI use plain CSS / CSS modules, no CSS framework. For EN/UZ text use simple JSON translation files with a small React context, no i18n library.
- Videos and files are stored with Django's media storage on the server. Paid files are served only after the backend checks enrolment.
- E-mail notifications use Django's built-in e-mail sending.
- If Stripe test mode can't be used from Uzbekistan, build a fake payment service with the same interface (`payments` app) so it can be swapped later.

## Repository structure (target)

```
/
├── CLAUDE.md
├── README.md
├── .gitignore
├── .env.example          # never commit the real .env
├── docker-compose.yml    # db + backend (+ frontend dev)
├── .github/workflows/ci.yml   # runs PyTest on every push / PR
├── docs/                 # requirements, user stories, diagrams (exported from Figma)
├── backend/
│   ├── manage.py
│   ├── config/           # Django project settings, urls, wsgi/asgi
│   ├── apps/
│   │   ├── accounts/     # custom User model, roles, auth
│   │   ├── courses/      # courses, lessons, enrolments, progress
│   │   ├── lectures/     # free open lectures (recorded + live)
│   │   ├── bookings/     # tutor & mentor profiles, availability, bookings, reviews
│   │   ├── placement/    # placement tests, questions, levels, matching/ranking
│   │   ├── payments/     # Stripe test mode / fake payment service
│   │   └── integrations/ # Zoom API client
│   ├── requirements.txt
│   ├── pytest.ini
│   └── Dockerfile
└── frontend/
    ├── src/
    │   ├── pages/  components/  api/  i18n/  context/
    ├── package.json
    └── Dockerfile
```

## Conventions

- **Custom user model** from day one: `accounts.User` (extends `AbstractUser`) with a `role` field. Set `AUTH_USER_MODEL` before the first migration.
- Settings come from environment variables (`.env`). Never hard-code secrets or commit `.env`.
- API lives under `/api/v1/`. Use DRF viewsets/serializers, and permissions per role.
- Every new backend feature gets PyTest tests in `apps/<app>/tests/`. Keep tests passing before committing.
- Bookings must never double-book a slot: use a database transaction plus a uniqueness/overlap check.
- Code style: PEP 8 for Python, clear names, short functions, comments where logic is not obvious. **The team must understand and defend every line at the evaluation**, so prefer simple, readable code over clever code. Explain what you changed and why after each task.
- Git: small commits with clear messages (`feat:`, `fix:`, `test:`, `docs:`, `chore:`). Work on feature branches and merge through pull requests.
- Development OS is **Windows** (PowerShell). Give Windows-friendly commands; use Docker for PostgreSQL.

## Team roles

- **Avazbek**: team lead, backend (API, auth, payments, matching, Zoom), DevOps (Docker, CI)
- **Shohruh**: frontend (React pages), UI/UX in Figma, open lectures section
- **Abdurahmon**: database design, booking module, testing, deployment

## Timeline and current status

| Iteration | Weeks | Goal |
|---|---|---|
| 1: Foundation & Design | Fall 2026 Wk 8–15 | Requirements, Figma wireframes, architecture + ER design, repo/Docker/CI setup, **registration + login with roles** |
| 2: Courses & Open Lectures | Spring 2027 Wk 1–5 | Course marketplace end to end, free open lectures, payments (test mode) |
| 3: Tutors, Mentors & Zoom | Spring 2027 Wk 6–10 | Tutor & mentor booking, Zoom links, placement test, matching, reviews, admin |
| 4: Evaluation & Submission | Spring 2027 Wk 11–15 | User testing (≥ 15 users, SUS ≥ 70), fixes, deployment, report |

**Current: Fall Week 10.** The mid evaluation is at the end of Fall Week 15. Plan for the rest of Iteration 1:
- Wk 10: requirements/user stories draft, repo skeleton (Django + React + Docker + PyTest)
- Wk 11: ER diagram and database models; Figma wireframes
- Wk 12: Docker Compose + GitHub Actions CI running PyTest; final architecture diagram
- Wk 13: registration, login (JWT) and roles: backend API
- Wk 14: login/registration pages in React connected to the API; tests
- Wk 15: bug fixes, demo, evaluation preparation

## Evaluation targets (keep in mind)

Task completion ≥ 90%; SUS ≥ 70; pages load < 3 s, API < 500 ms; ≥ 70% backend test coverage; no critical OWASP Top 10 issues; role-based access on every endpoint.
## Git rules
- Never push, merge, or force-push. Commit on feature branches only; the team pushes and merges.
- Never commit .env or any secrets.
- Never delete files or run destructive commands without asking first.