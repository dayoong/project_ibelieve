from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
relations = Table('relations', post_meta,
    Column('child_id', Integer),
    Column('parent_id', Integer),
)

user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('role', INTEGER),
    Column('related_user1', INTEGER),
    Column('related_user2', INTEGER),
    Column('nickname', TEXT(length=80)),
    Column('phone', VARCHAR(length=50)),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('role', Integer),
    Column('nickname', UnicodeText(length=80)),
    Column('email', String(length=120)),
    Column('phone', String(length=50)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['relations'].create()
    pre_meta.tables['user'].columns['related_user1'].drop()
    pre_meta.tables['user'].columns['related_user2'].drop()
    post_meta.tables['user'].columns['email'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['relations'].drop()
    pre_meta.tables['user'].columns['related_user1'].create()
    pre_meta.tables['user'].columns['related_user2'].create()
    post_meta.tables['user'].columns['email'].drop()
