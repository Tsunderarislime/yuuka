import discord as ds
from datetime import datetime
from time import mktime
import sqlalchemy as sa

# Create a database for a server
def initialize(guild):
    engine = sa.create_engine('sqlite:///database/' + str(guild.id) + '.sqlite')
    conn = engine.connect()
    metadata = sa.MetaData()
    now = datetime.utcnow().timestamp()

    # Table for users that will not be considered as spam
    user = sa.Table(
        'User', metadata,
        sa.Column('Id', sa.Integer(), primary_key=True)
    )

    # Table for words which will be checked in messages sent from potential spam
    word = sa.Table(
        'Word', metadata,
        sa.Column('Word', sa.String(255), nullable=False),
        sa.Column('Weight', sa.Integer(), default=1)
    )

    # Create the tables
    metadata.create_all(engine)

    # If it has been over 3 weeks since a member has joined when initializing the database, then mark them as safe (not great, but fast)
    for member in guild.members:
        if now - mktime(member.joined_at.timetuple()) > 1814400:
            query = sa.insert(user).values(Id=member.id)
            conn.execute(query)

    # Save changes to database, then clean up
    conn.commit()
    conn.close()
    engine.dispose()