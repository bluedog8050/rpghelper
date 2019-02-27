import discord
from discord.ext import commands
import logging
import os

logging.basicConfig(level = logging.INFO)

#Print Copyright disclaimer
print('''Reverb Bot  Copyright (C) 2018  Derek Peterson
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions; see LICENSE file for more information.''')

with open('bot.key') as k:
    token = k.read()

bot = commands.Bot('!', pm_help = True)

# this specifies what extensions to load when the bot starts up (found in cogs folder)
extensions_dir = os.listdir(os.path.abspath('./cogs/'))
startup_extensions = [x[:-3] for x in extensions_dir if not x.startswith('__') and x.endswith('.py')]
logging.info(f'Loading startup cogs: {startup_extensions}')
#startup_extensions = ['reverb', 'turntracker', 'gamecommands', 'debug']

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
@commands.has_permissions(administrator = True)
async def load(ctx, extension_name : str):
    '''Loads an extension.'''
    try:
        bot.load_extension('cogs.' + extension_name)
    except (AttributeError, ImportError) as e:
        await ctx.send(f'```py\n{type(e).__name__}: {str(e)}\n```')
        return
    await ctx.send(f'{extension_name} loaded.')

@bot.command()
@commands.has_permissions(administrator = True)
async def unload(ctx, extension_name : str):
    '''Unloads an extension.'''
    bot.unload_extension(extension_name)
    await ctx.send(f'{extension_name} unloaded.')

@bot.command()
@commands.has_permissions(administrator = True)
async def reload(ctx, extension_name : str):
    '''Reloads an extension.'''
    bot.unload_extension(extension_name)
    await ctx.send(f'{extension_name} unloaded.')
    try:
        bot.load_extension('cogs.' + extension_name)
    except (AttributeError, ImportError) as e:
        await ctx.send(f'```py\n{type(e).__name__}: {str(e)}\n```')
        return
    await ctx.send(f'{extension_name} loaded.')

if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension('cogs.' + extension)
        except Exception as e:
            exc = f'{type(e).__name__}: {e}'
            logging.info(f'Failed to load extension {extension}\n{exc}')

bot.run(token)