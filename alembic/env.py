from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def upgrade(migrate_engine):
    # create freebies table
    freebies = Table(
        'freebies', Base.metadata,
        Column('id', Integer, primary_key=True),
        Column('item_name', String),
        Column('value', Integer),
        Column('company_id', Integer, ForeignKey('companies.id')),
        Column('dev_id', Integer, ForeignKey('devs.id')),
    )
    freebies.create(migrate_engine)

def downgrade(migrate_engine):
    freebies = Table('freebies', Base.metadata, autoload_with=migrate_engine)
    freebies.drop(migrate_engine)
