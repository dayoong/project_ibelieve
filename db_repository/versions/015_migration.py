from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
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
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('role', Integer),
    Column('nickname', String(length=80)),
    Column('email', String(length=120)),
    Column('phone', String(length=50)),
    Column('last_seen', DateTime),
    Column('future_goal', String(length=100)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['goal'].create()
    post_meta.tables['user'].columns['future_goal'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['goal'].drop()
    post_meta.tables['user'].columns['future_goal'].drop()
