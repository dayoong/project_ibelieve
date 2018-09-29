from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
notification = Table('notification', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('post_id', Integer),
    Column('get_id', Integer),
    Column('goal_id', Integer),
    Column('contents', String(length=200)),
    Column('badge', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['notification'].columns['badge'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['notification'].columns['badge'].drop()
