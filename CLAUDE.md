# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run development server
python manage.py runserver

# Apply migrations
python manage.py migrate

# Create migrations after model changes
python manage.py makemigrations

# Run tests
python manage.py test
```

**Dependencies** (no requirements.txt — install manually):
```bash
pip install django==5.1.5 requests
```

## Architecture

Single-app Django project. The `weather/` app contains all logic; `city_weather/` is the Django project config package.

**Request flow:**
1. User POSTs city name + type (`current` or `forecast`) from `index.html`
2. `weather/views.py:index()` geocodes the city via OpenWeatherMap Geo API (`/geo/1.0/direct`)
3. Depending on type, calls either `/data/2.5/weather` (current) or `/data/2.5/forecast` (first 8 entries)
4. Passes weather fields (temp, humidity, pressure, wind, description, icon) to the template

**Key files:**
- `weather/views.py` — all business logic and API calls
- `weather/urls.py` — app routes (`/` → `index`)
- `weather/templates/weather/index.html` — single-page UI
- `city_weather/settings.py` — Django config (DEBUG=True, SQLite)

**External API:** OpenWeatherMap — API key is currently hardcoded in `views.py`. Metric units (Celsius).

**Database:** SQLite (`db.sqlite3`). Models are currently empty; no weather data is persisted.
