# ParkIt - Flask + SQLAlchemy

## Setup (exact commands)

# 1. Create venv
python3 -m venv venv

# 2. Activate venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set FLASK_APP so Flask CLI can discover your app
export FLASK_APP=app.py    # on PowerShell: $env:FLASK_APP="app.py"

# 5. Initialize migrations (first time only)
flask db init

# 6. Create & apply migration
flask db migrate -m "initial migration"
flask db upgrade

# 7. Seed the database
python seed.py

# 8. Run server
flask run
# Open: http://127.0.0.1:5000/

## Endpoints
- GET  /           -> welcome + endpoints list
- GET  /users
- POST /users      -> payload: { "name": "...", "email": "..." }
- DELETE /users/<id>

- GET  /spots
- POST /spots      -> payload: { "name": "...", "location": "...", "available": true }
- PATCH /spots/<id> -> update fields name/location/available
- DELETE /spots/<id>

- GET  /reservations
- POST /reservations -> payload: { "user_id": 1, "spot_id": 2 }
- DELETE /reservations/<id>
