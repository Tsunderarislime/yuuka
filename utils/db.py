import discord as ds
from datetime import datetime
from time import mktime
import sqlalchemy as sa
import os

# Create a database for a server
def initialize(guild, channel_id):
    print('Initializing database...')
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

    # May as well use a table to store config values
    config = sa.Table(
        'Config', metadata,
        sa.Column('Name', sa.String(255), nullable=False),
        sa.Column('Value', sa.Integer())
    )

    # Create the tables
    metadata.create_all(engine)

    # If it has been over 3 weeks since a member has joined when initializing the database, then mark them as safe (not great, but fast)
    for member in guild.members:
        if now - mktime(member.joined_at.timetuple()) > 1814400:
            query = sa.insert(user).values(Id=member.id)
            conn.execute(query)
    
    # Set the default threshold of 10, default channel as the one where the initialization command was called. Starts disabled
    query = sa.insert(config)
    conn.execute(query, [{'Name': 'Threshold', 'Value': 10}, {'Name': 'Channel', 'Value': channel_id}, {'Name': 'Active', 'Value': 0}])

    # Save changes to database, then clean up
    conn.commit()
    conn.close()
    engine.dispose()


# Check if a database even exists
def exists(id):
    return os.path.exists('database/' + str(id) + '.sqlite')