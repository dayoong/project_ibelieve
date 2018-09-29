from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
tmp_enrollment = Table('tmp_enrollment', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('user_id', INTEGER),
    Column('related_phone', VARCHAR(length=50)),
)

temp = Table('temp', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('related_phone', String(length=50)),
)

user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('role', INTEGER),
    Column('related_user', INTEGER),
    Column('nickname', TEXT(length=80)),
    Column('phone', VARCHAR(length=50)),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('role', Integer),
    Column('related_user1', Integer),
    Column('related_user2', Integer),
    Column('nickname', UnicodeText(length=80)),
    Column('phone', String(length=50)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['tmp_enrollment'].drop()
    post_meta.tables['temp'].create()
    pre_meta.tables['user'].columns['related_user'].drop()
    post_meta.tables['user'].columns['related_user1'].create()
    post_meta.tables['user'].columns['related_user2'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['tmp_enrollment'].create()
    post_meta.tables['temp'].drop()
    pre_meta.tables['user'].columns['related_user'].create()
    post_meta.tables['user'].columns['related_user1'].drop()
    post_meta.tables['user'].columns['related_user2'].drop()
