from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
reward = Table('reward', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('parent_id', Integer),
    Column('child_id', Integer),
    Column('parent_status', String(length=5)),
    Column('child_status', String(length=5)),
    Column('contents', String(length=50)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['reward'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['reward'].drop()
