import discord as ds
import sqlalchemy as sa

# List commands for the filter command
def help():
    embed = ds.Embed(title='📋 Filter Command Usage 📋',
        description='`y^filter` summons this information box.',
        color=ds.Color.magenta()
    )
    embed.add_field(name='Add word to filter (or update weight)', value='`y^filter add <word> <weight>`', inline=False)
    embed.add_field(name='Remove word from filter', value='`y^filter remove <word>`', inline=False)
    embed.add_field(name='List all words/values in filter', value='`y^filter list <page>`', inline=False)
    embed.add_field(name='Change the message spam threshold', value='`y^filter threshold <value>`', inline=False)
    embed.add_field(name='Change the channel for ban notifications', value='`y^filter channel <channel_id>`', inline=False)
    embed.add_field(name='Activate/deactivate the filter', value='`y^filter active <0 or 1>`', inline=False)
    embed.add_field(name='Check the current threshold and channel', value='`y^filter current`', inline=False)

    return embed

# Add a word to the filter or update a word's weight in the filter
def add(id, word, weight):
    # Make sure the word is not empty whitespace and that the weight given is greater than 0
    # The int cast should also catch non-number weights
    assert(bool(word.strip()) and int(weight) > 0)

    # Access the database for the respective server id
    engine = sa.create_engine('sqlite:///database/' + str(id) + '.sqlite')
    conn = engine.connect()
    metadata = sa.MetaData()

    # Get the words table
    word_table = sa.Table('Word', metadata, autoload_with=engine)

    # Check if the word already exists
    query = word_table.select().where(word_table.columns.Word == word.lower())
    output = conn.execute(query)

    if output.fetchone() is not None:
        # Word already exists in table, update the weight
        query = word_table.update().values(Weight=weight).where(word_table.columns.Word == word.lower())
        flag = True
    else:
        # Word is not in table, add it to the table
        query = sa.insert(word_table).values(Word=word.lower(), Weight=weight)
        flag = False
        
    # Add word to table or update the word already in the table
    conn.execute(query)

    # Save changes to database, then clean up
    conn.commit()
    conn.close()
    engine.dispose()

    # Return a boolean to determine what message to send upon completion
    return flag

# Remove a word if it is in the filter
def remove(id, word):
    # Make sure the word is not empty whitespace
    assert(bool(word.strip()))

    # Access the database for the respective server id
    engine = sa.create_engine('sqlite:///database/' + str(id) + '.sqlite')
    conn = engine.connect()
    metadata = sa.MetaData()

    # Get the words table
    word_table = sa.Table('Word', metadata, autoload_with=engine)

    # Check if the word already exists
    query = word_table.select().where(word_table.columns.Word == word.lower())
    output = conn.execute(query)

    if output.fetchone() is not None:
        # Delete the word in the table
        query = word_table.delete().where(word_table.columns.Word == word.lower())
        conn.execute(query)
        flag = True
    else:
        # Word was not in the table
        flag = False

    # Save changes to database, then clean up
    conn.commit()
    conn.close()
    engine.dispose()

    # Return a boolean to determine what message to send upon completion
    return flag

# Lists all of the words currently in the filter
def list(id, page=1):
    # Lazy assert, if number too high it just caps at the highest page number
    assert(int(page) > 0)
    # Access the database for the respective server id
    engine = sa.create_engine('sqlite:///database/' + str(id) + '.sqlite')
    conn = engine.connect()
    metadata = sa.MetaData()

    # Get the config table
    word_table = sa.Table('Word', metadata, autoload_with=engine)

    # Update the value of the specified config in the table
    query = word_table.select()
    result = conn.execute(query).fetchall()

    # If the result is empty
    if not result:
        embed = ds.Embed(title='ℹ️ 0 Words in the Filter ℹ️',
            description='There are no words in the word filter',
            color=ds.Color.magenta()
        )
    else:
        # Create embed for the list of words
        embed = ds.Embed(title=f'ℹ️ {len(result)} Words in the Filter ℹ️',
            description='This embed will show up to 15 words',
            color=ds.Color.magenta()
        )
        # Highest page number possible
        max_page = (len(result) // 15) + (len(result) % 15 > 0)
        # The page to use in looping
        pg = min(int(page), max_page)

        # Set the footer as the page number
        embed.set_footer(text=f'Page {pg}/{max_page}')

        # Loop through results at the specified page
        for i in range(15*(pg-1), min(15*pg, len(result))):
            embed.add_field(name=result[i][0], value=result[i][1], inline=True)

    # Clean up database
    conn.close()
    engine.dispose()

    # Return embed
    return embed


# Update the threshold/channel ID
def config(id, name, value):
    # Make that the value given is greater than 0. The int cast should also catch non-number values
    assert(bool(int(value) >= 0))

    # Access the database for the respective server id
    engine = sa.create_engine('sqlite:///database/' + str(id) + '.sqlite')
    conn = engine.connect()
    metadata = sa.MetaData()

    # Get the config table
    config_table = sa.Table('Config', metadata, autoload_with=engine)

    # Update the value of the specified config in the table
    v = (min(1, int(value))) if name == 'Active' else int(value)
    query = config_table.update().values(Value=v).where(config_table.columns.Name == name)
    conn.execute(query)

    # Save changes to database, then clean up
    conn.commit()
    conn.close()
    engine.dispose()

    # Flag to return for toggling the 'active' 
    return bool(v)

# Check current threshold and channel ID
def current(id):
    # Access the database for the respective server id
    engine = sa.create_engine('sqlite:///database/' + str(id) + '.sqlite')
    conn = engine.connect()
    metadata = sa.MetaData()

    # Get the config table
    config_table = sa.Table('Config', metadata, autoload_with=engine)

    # Update the value of the specified config in the table
    query = config_table.select()
    result = conn.execute(query).fetchall()

    # Create embed for the config
    embed = ds.Embed(title='ℹ️ Current Configuration ℹ️',
        description='Here is the current configuration of the filter.',
        color=ds.Color.magenta()
    )

    # Loop through results
    for row in result:
        embed.add_field(name=row[0], value=row[1], inline=True)

    # Clean up database
    conn.close()
    engine.dispose()

    # Return embed
    return embed