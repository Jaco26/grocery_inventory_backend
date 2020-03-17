# write sqlalchemy script to seed fresh database with necessary entries

import click
from flask.cli import with_appcontext

from app.database.db import db
from app.database.models import (
  PackagingState,
  PackagingKind,
)


@click.command('seed-db')
@with_appcontext
def seed_db():
  db.session.add_all([
    PackagingKind(name="N/A", uniform_name="n/a"),
    PackagingKind(name="Prepackaged Glass Jar", uniform_name="prepackaged_glass_jar"),
    PackagingKind(name="Plastic Produce Bag", uniform_name="plastic_produce_bag"),
    PackagingKind(name="Mason Jar", uniform_name="mason_jar"),
    PackagingKind(name="Prepackaged Cardbord Box", uniform_name="prepackaged_cardboard_box"),
  ])

  db.session.add_all([
    PackagingState(name="N/A", uniform_name="n/a"),
    PackagingState(name="Unopened", uniform_name="unopened"),
    PackagingState(name="Disgarded", uniform_name="disgarded"),
    PackagingState(name="Opened", uniform_name="opened"),
  ])

  db.session.commit()


