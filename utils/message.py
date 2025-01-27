import discord as ds
import sqlalchemy as sa
import string

# Check if the author of the message is in the trusted users database
def check(message):
    # Access the database for the respective server id
    engine = sa.create_engine('sqlite:///database/' + str(message.guild.id) + '.sqlite')
    conn = engine.connect()
    metadata = sa.MetaData()

    # Get the users table
    user_table = sa.Table('User', metadata, autoload_with=engine)

    # Check if the word already exists
    query = user_table.select().where(user_table.columns.Id == message.author.id)
    output = conn.execute(query)

    # Flag which indicates a spam message
    flag = False

    if output.fetchone() is not None:
        # User is in table, return the false flag (and values that won't be used)
        return flag, 0, 0, 0
    else:
        # User is not in table, begin evaluating the message content
        score = 0

        # Get the words and config table
        word_table = sa.Table('Word', metadata, autoload_with=engine)
        config_table = sa.Table('Config', metadata, autoload_with=engine)

        # Get the threshold for a message to be considered spam
        config = conn.execute(config_table.select()).fetchall()
        threshold = config[0][1]
        log_id = config[1][1]

        # Break down the message content into individual words
        words = message.content.strip().split(' ')

        # Begin scoring
        for word in words:
            # Remove any punctuation leftover in each word and lowercase all letters
            w = word.translate(str.maketrans('', '', string.punctuation)).lower()

            # Check if the word is in the filter
            query = word_table.select().where(word_table.columns.Word == w)
            result = conn.execute(query).fetchall()
            if result:
                # Word is in the filter, add the weight to the score
                score += result[0][1]

        if score >= threshold:
            # The message is considered spam
            flag = True
        else:
            # The message is not considered spam, add this user to the trusted user database
            query = sa.insert(user_table).values(Id=message.author.id)
            conn.execute(query)
    
    # Save changes to database, then clean up
    conn.commit()
    conn.close()
    engine.dispose()

    # Return a boolean to determine what action to take
    return flag, score, threshold, log_id

# Check if the filter is active
def active(id):
    # Access the database for the respective server id
    engine = sa.create_engine('sqlite:///database/' + str(id) + '.sqlite')
    conn = engine.connect()
    metadata = sa.MetaData()

    # Get the config table
    config_table = sa.Table('Config', metadata, autoload_with=engine)

    # Update the value of the specified config in the table
    query = config_table.select().where(config_table.columns.Name == 'Active')
    result = conn.execute(query).fetchall()[0][1]

    # Clean up database
    conn.close()
    engine.dispose()

    # Return boolean
    return result