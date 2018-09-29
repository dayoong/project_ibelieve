from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
letter = Table('letter', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('parent', Integer),
    Column('child', Integer),
    Column('contents', String(length=500)),
    Column('timestamp', String(length=15)),
)

notification = Table('notification', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('post_id', Integer),
    Column('get_id', Integer),
    Column('goal_id', Integer),
    Column('contents', String(length=200)),
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
    Column('self_evaluation', String(length=140)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['letter'].create()
    post_meta.tables['notification'].columns['goal_id'].create()
    post_meta.tables['goal'].columns['self_evaluation'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['letter'].drop()
    post_meta.tables['notification'].columns['goal_id'].drop()
    post_meta.tables['goal'].columns['self_evaluation'].drop()
