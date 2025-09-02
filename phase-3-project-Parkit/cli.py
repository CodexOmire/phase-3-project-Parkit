import click
from app import create_app
from db import db
from models import User, ParkingSpot, Reservation


app = create_app()


def ensure_tables():
    with app.app_context():
        db.create_all()


@click.group()
def cli():
    """ParkIt CLI commands."""
    pass


@cli.command()
def db_create():
    """Create all database tables."""
    ensure_tables()
    click.echo("Database tables created.")


@cli.command()
def db_drop():
    """Drop all database tables."""
    with app.app_context():
        db.drop_all()
        click.echo("Database tables dropped.")


@cli.command()
def seed():
    """Seed database with sample data."""
    from seed import seed_data
    seed_data(app)
    click.echo("Database seeded.")


@cli.command()
@click.option("--name", prompt=True, help="User name")
@click.option("--email", prompt=True, help="User email")
def create_user(name: str, email: str):
    """Create a user."""
    ensure_tables()
    with app.app_context():
        if User.query.filter_by(email=email).first():
            click.echo("Email already exists.")
            return
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()
        click.echo(f"Created user id={user.id}")


@cli.command()
def list_parking():
    """List all parking spots."""
    ensure_tables()
    with app.app_context():
        spots = ParkingSpot.query.all()
        for s in spots:
            click.echo(f"{s.id}: {s.name} - {s.location} (available={s.available})")


@cli.command()
@click.option("--user-id", type=int, prompt=True, help="User ID")
@click.option("--spot-id", type=int, prompt=True, help="Spot ID")
def book_spot(user_id: int, spot_id: int):
    """Book a parking spot for a user."""
    ensure_tables()
    with app.app_context():
        user = User.query.get(user_id)
        spot = ParkingSpot.query.get(spot_id)
        if not user:
            click.echo("User not found.")
            return
        if not spot:
            click.echo("Spot not found.")
            return
        if not spot.available:
            click.echo("Spot is not available.")
            return
        reservation = Reservation(user_id=user.id, spot_id=spot.id)
        db.session.add(reservation)
        spot.available = False
        db.session.commit()
        click.echo(f"Booked reservation id={reservation.id}")


if __name__ == "__main__":
    cli()

