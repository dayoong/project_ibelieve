from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
letter = Table('letter', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('parent', Integer),
    Column('parent_nickname', String(length=80)),
    Column('child', Integer),
    Column('child_nickname', String(length=80)),
    Column('contents', String(length=500)),
    Column('timestamp', String(length=15)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['letter'].columns['child_nickname'].create()
    post_meta.tables['letter'].columns['parent_nickname'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['letter'].columns['child_nickname'].drop()
    post_meta.tables['letter'].columns['parent_nickname'].drop()
