from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
relations = Table('relations', pre_meta,
    Column('child_id', INTEGER),
    Column('parent_id', INTEGER),
)

relationship = Table('relationship', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('child', Integer),
    Column('parent', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['relations'].drop()
    post_meta.tables['relationship'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['relations'].create()
    post_meta.tables['relationship'].drop()
