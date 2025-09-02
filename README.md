# ParkIt - Flask + SQLAlchemy

## Setup (exact commands)

# 1. Create venv
python3 -m venv venv

# 2. Activate venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Navigate into project and set FLASK_APP (app factory)
cd phase-3-project-Parkit
export FLASK_APP='app:create_app'    # PowerShell: $env:FLASK_APP='app:create_app'

# 5. Initialize migrations (first time only)
flask db init

# 6. Create & apply migration
flask db migrate -m "initial migration"
flask db upgrade

# 7. Seed the database (via Flask CLI)
flask seed

# 8. Run server
flask run
# Open: http://127.0.0.1:5000/

## CLI helpers
- flask db_create  -> create tables
- flask db_drop    -> drop tables
- flask seed       -> drop, create, seed sample data

## Endpoints
- GET  /                    -> welcome + endpoints list

- GET  /users               -> list users
- POST /users               -> { name, email }
- GET  /users/<id>          -> user by id
- PATCH /users/<id>         -> { name?, email? }
- DELETE /users/<id>

- GET  /spots               -> list spots
- POST /spots               -> { name, location, available? }
- GET  /spots/<id>          -> spot by id
- PATCH /spots/<id>         -> { name?, location?, available? }
- DELETE /spots/<id>

- GET  /reservations        -> list reservations
- POST /reservations        -> { user_id, spot_id }
- GET  /reservations/<id>   -> reservation by id
- PATCH /reservations/<id>  -> { end_time? as ISO8601 }
- DELETE /reservations/<id>
