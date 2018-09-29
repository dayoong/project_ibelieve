from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
post = Table('post', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('body', VARCHAR(length=1000)),
    Column('timestamp', DATETIME),
    Column('user_id', INTEGER),
)

goal = Table('goal', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user', Integer),
    Column('timestamp', String(length=15)),
    Column('contents', String(length=20)),
    Column('start_date', String(length=10)),
    Column('start_day', String(length=10)),
    Column('start_hour', Integer),
    Column('start_minute', Integer),
    Column('finish_date', String(length=10)),
    Column('finish_day', String(length=10)),
    Column('finish_hour', Integer),
    Column('finish_minute', Integer),
    Column('alert_time', Integer),
    Column('alert_cycle', String(length=10)),
    Column('color', String(length=10)),
    Column('memo', String(length=150)),
    Column('status', String(length=10)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].drop()
    post_meta.tables['goal'].columns['status'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].create()
    post_meta.tables['goal'].columns['status'].drop()
