import click
from flask.cli import with_appcontext


@click.group()
def cli():
    """Main entry point"""


@cli.command("init")
@with_appcontext
def init():
    """Create a new admin user"""
    from src.extensions import db
    from src.models import User

    click.echo("create user")
    user = User(username="w0rng", email="antonabramov2000@gmail.com", password="1", active=True)
    db.session.add(user)
    db.session.commit()
    click.echo("created user admin")


if __name__ == "__main__":
    cli()
