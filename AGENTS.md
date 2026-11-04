# AGENTS.md

## Project overview
This repository is a Django portfolio website for Tiffany Ekklesia. It includes:
- Django app: `main/`
- project settings: `portofolio/`
- templates and static assets
- a DRF API used by the AJAX-based Projects page

## Key commands
Use the project virtual environment when running local Django commands:

```powershell
cd C:\Users\tiffa\OneDrive\Documents\GitHub\myportofolio
.\env\Scripts\Activate.ps1
python manage.py migrate
python manage.py test main.tests_api -v 2
python manage.py runserver
```

## Important implementation notes
- The portfolio API is under `main/api_views.py` and `main/api_urls.py`.
- The DRF serializer contract is defined in `main/serializers.py`.
- For project stars, the canonical field is `starred_by` (not `stars`) to match the tutorial contract and serializer expectations.
- Protected API actions are controlled by `main/permissions.py`.
- The frontend AJAX page is in `templates/project.html` and should keep using the `api:project-*` routes.

## Validation workflow
Before finishing work:
1. Run the relevant Django tests.
2. Verify the API still returns JSON in the expected format.
3. Check that authenticated/anonymous permission behavior still matches the tutorial requirements.

## Deployment notes
- Production settings are controlled by environment variables and `PRODUCTION` in `portofolio/settings.py`.
- The project has remotes configured for both GitHub (`origin`) and PWS (`pws`).
- For PWS deployment, keep `ALLOWED_HOSTS` and DB configuration aligned with the target environment.

## Coding conventions
- Keep names consistent with the tutorial contract (`project-list`, `project-detail`, `project-star`).
- Prefer minimal changes that preserve the existing portfolio behavior.
- If a model field is renamed, add/update the migration file and verify tests.

## AI usage guidance
Future AI assistants should:
- treat this repo as a Django portfolio app, not a generic API starter.
- prefer the existing project patterns and naming conventions over inventing new ones.
- keep API endpoints backward-compatible with the frontend unless the tutorial explicitly requires a format change.
- validate with Django tests before claiming the task is finished.
