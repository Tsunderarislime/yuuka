import discord as ds

# List all of the commands
def help():
    embed = ds.Embed(title='💡 Help 💡',
        description='Here\'s a list of commands.',
        color=ds.Color.green()
    )
    embed.add_field(name='Information ℹ️', value='- `help`\n- `github`', inline=True)
    embed.add_field(name='Filter ⛔', value='- `initialize`\n- `filter`', inline=True)

    return embed

# Github repository link
def github():
    embed = ds.Embed(title='GitHub Repository',
        url='https://github.com/Tsunderarislime/yuuka',
        description='Here\'s the link to my GitHub repository.',
        color=ds.Color.green()
    )

    return embed