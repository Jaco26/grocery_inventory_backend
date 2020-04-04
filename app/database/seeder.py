# write sqlalchemy script to seed fresh database with necessary entries

import click
from flask.cli import with_appcontext

from app.database.db import db
from app.database.models import (
  PackagingState,
  PackagingKind,
  UnitOfMeasurement,
)


@click.command('seed-db')
@with_appcontext
def seed_db():
  db.session.add_all([
    PackagingKind(name="N/A"),
    PackagingKind(name="Prepackaged Glass Jar"),
    PackagingKind(name="Plastic Produce Bag"),
    PackagingKind(name="Mason Jar"),
    PackagingKind(name="Prepackaged Cardbord Box"),
  ])

  db.session.add_all([
    PackagingState(name="N/A"),
    PackagingState(name="Unopened"),
    PackagingState(name="Disgarded"),
    PackagingState(name="Opened"),
  ])
  db.session.add_all([
    UnitOfMeasurement(name="Self"),
    UnitOfMeasurement(name="Fluid Oz"),
    UnitOfMeasurement(name="Oz"),
    UnitOfMeasurement(name="Cup"),
  ])

  db.session.commit()


