# ParkIt

## Requirements
- Python 3.8+
- SQLite (default)

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Database & App
- Config: `config.py` with SQLite URI
- SQLAlchemy initialization: `db.py`
- Models: `models/` plus `models.py` aggregator
- App factory: `app.create_app()` registers blueprints and errors

## CLI
Commands are implemented in `cli.py` using Click.

Examples:
```bash
python cli.py db-create
python cli.py seed
python cli.py create-user --name "Alice" --email alice@example.com
python cli.py list-parking
python cli.py book-spot --user-id 1 --spot-id 2
```

## Flask server
```bash
export FLASK_APP='app:create_app'
flask run
```

## Seeding
```bash
python cli.py seed
```

## Testing
```bash
pip install pytest
pytest -q
```

## Project Structure
```
phase-3-project-Parkit
├── app.py
├── cli.py
├── config.py
├── db.py
├── models/
├── models.py
├── routes/
├── seed.py
├── tests/
├── requirements.txt
└── README.md
```

