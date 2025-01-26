import discord as ds
from discord.ext import commands as cd
import utils.info
import utils.db

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


# MAIN FUNCTIONS
 
# Initialize a database for the automated spam deletion. Use this immediately after the bot is added to the server
@bot.command()
@cd.has_permissions(manage_guild=True)
async def initialize(ctx):
    utils.db.initialize(ctx.guild)
    await ctx.send('Completed the database initialization.')

@initialize.error
async def initialize_error(ctx, error):
    pass


'''

RUNNING THE BOT

'''

# Read the authentication token for the bot
with open('token.txt') as f:
    token = f.readline()
    f.close()

# Run the bot
bot.run(token)