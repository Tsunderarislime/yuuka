import discord as ds
from discord.ext import commands as cd
import utils.info
import utils.db
import utils.filter
import utils.message

'''

INITIALIZATION

'''

# Standard bot initialization stuff
intents = ds.Intents.default()
intents.members = True
intents.moderation = True
intents.message_content = True
bot = cd.Bot(command_prefix='y^', intents=intents, activity=ds.Game(name="y^help"))

# Print to console upon successful login
@bot.event
async def on_ready():
    print(f'Successfully logged in as {bot.user}')

# Removing the default help command, a custom help command will take its place
bot.remove_command('help')

'''

COMMANDS

'''

# INFORMATION

# List of every command available
@bot.command()
@cd.has_permissions(manage_guild=True)
async def help(ctx):
    embed = utils.info.help()
    await ctx.send(embed=embed)

@help.error
async def help_error(ctx, error):
    # No need to do anything for those without perms, this is just here to stop the console from getting spammed with error messages
    pass

# Github repository link for the bot
@bot.command()
@cd.has_permissions(manage_guild=True)
async def github(ctx):
    embed = utils.info.github()
    await ctx.send(embed=embed)

@github.error
async def github_error(ctx, error):
    pass


# DATABASE AND FILTER
 
# Initialize a database for the automated spam deletion. Use this immediately after the bot is added to the server
@bot.command()
@cd.has_permissions(manage_guild=True)
async def initialize(ctx):
    t = utils.db.initialize(ctx.guild, ctx.channel.id)
    await ctx.send(f'Completed the database initialization in {t:.3f} seconds.')

@initialize.error
async def initialize_error(ctx, error):
    pass

@bot.command()
@cd.has_permissions(manage_guild=True)
async def filter(ctx, *args):
    # Do nothing if the database doesn't even exist
    if not utils.db.exists(ctx.guild.id):
        await ctx.send('Run `y^initialize` first before this command can be used.')
        return
    
    # Send help dialogue if no arguments are passed
    if len(args) < 1:
        await ctx.send(embed=utils.filter.help())
    else:
        match args[0]:
            case 'add':
                try:
                    # Attempt to run the add() command
                    if utils.filter.add(ctx.guild.id, args[1], args[2]):
                        await ctx.send(f'ℹ️ Updated the weight of `{args[1]}`. ℹ️')
                    else:
                        await ctx.send(f'➕ Added `{args[1]}` to the filter. ➕')
                except Exception as e:
                    print(e)
                    await ctx.send('Invalid arguments given. See `y^filter` for command usage.')

            case 'remove':
                try:
                    # Attempt to run the add() command
                    if utils.filter.remove(ctx.guild.id, args[1]):
                        await ctx.send(f'➖ Removed `{args[1]}` from the filter. ➖')
                    else:
                        await ctx.send(f'🟰 `{args[1]}` was not in the filter. 🟰')
                except Exception as e:
                    print(e)
                    await ctx.send('Invalid arguments given. See `y^filter` for command usage.')

            case 'list':
                try:
                    # Attempt to run the list() command
                    await ctx.send(embed=utils.filter.list(ctx.guild.id, args[1]))
                except Exception as e:
                    print(e)
                    await ctx.send('Invalid arguments given. See `y^filter` for command usage.')

            case 'threshold':
                try:
                    # Attempt to run the config() command for threshold
                    utils.filter.config(ctx.guild.id, args[0].capitalize(), args[1])
                    await ctx.send(f'ℹ️ Updated the {args[0]}. ℹ️')
                except Exception as e:
                    print(e)
                    await ctx.send('Invalid arguments given. See `y^filter` for command usage.')

            case 'channel':
                try:
                    # Attempt to run the config() command for channel ID
                    utils.filter.config(ctx.guild.id, args[0].capitalize(), args[1])
                    await ctx.send(f'ℹ️ Updated the {args[0]} ID. ℹ️')
                except Exception as e:
                    print(e)
                    await ctx.send('Invalid arguments given. See `y^filter` for command usage.')
            
            case 'active':
                try:
                    # Attempt to run the config() command for channel ID
                    if utils.filter.config(ctx.guild.id, args[0].capitalize(), args[1]):
                        await ctx.send('⛔ The spam filter is active. ⛔')
                    else:
                        await ctx.send('✅ The spam filter is inactive. ✅')
                except Exception as e:
                    print(e)
                    await ctx.send('Invalid arguments given. See `y^filter` for command usage.')
            
            case 'current':
                await ctx.send(embed=utils.filter.current(ctx.guild.id))
            
            case _:
                await ctx.send(f'Invalid command `{args[0]}`!')


@filter.error
async def filter_error(ctx, error):
    pass


'''

MESSAGE EVENT LISTENER

'''

# Message content is passed to the evaluation function
# IDs in the user database should be exempt from any kind of punishment
@bot.event
async def on_message(message):
    # Do nothing if the bot is the one sending the message OR if the database has yet to exist yet OR if the filter is not active
    if message.author == bot.user or not utils.db.exists(message.guild.id) or not utils.message.active(message.guild.id):
        await bot.process_commands(message)
    else:
        # Check the message and determine the course of action based on the flag
        flag, score, threshold, log_id = utils.message.check(message)

        if flag:
            # Print to console
            print(f'Banned user {message.author.id}. Message score was {score}, which exceeded the threshold of {threshold}.')

            # Print to mod log channel
            await bot.get_channel(log_id).send(f'Banned <@{message.author.id}> `{message.author.id}` for posting spam. The message score was {score}, which exceeded the threshold of {threshold}. Their message was:\n `{message.content}`')

            # Do the deed
            await message.author.ban(delete_message_days=7)
        else:
            # Do nothing as the check function determined the message was not spam and/or was from a trusted user
            await bot.process_commands(message)


'''

RUNNING THE BOT

'''

# Read the authentication token for the bot
with open('token.txt') as f:
    token = f.readline()
    f.close()

# Run the bot
bot.run(token)