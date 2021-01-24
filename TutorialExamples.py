import discord
import json
import os
import random
from discord.ext import commands, tasks
from itertools import cycle
#specify's the bot's prefix.
client = commands.Bot(command_prefix = '.')
#variables for the background task test methods.
status= ['online', 'idle', 'dnd', 'invisible']
cycle_status = cycle(status)


#basic bot operations such as displaying text in cmd and as a reply.
@client.event
async def on_ready():
    #await client.change_presence(status=discord.Status.idle, activity=discord.Game('.help'))
    change_status.start()
    print('Bot is ready')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong {round(client.latency * 1000)}ms')

@client.command()
async def shelp(ctx):
    await ctx.send(f'ping: replies with the word pong and bot latency\ntest: replies to your question\nclear: clears specified number of pervious messages (default 5)')

#Take not of the aliase used. Can be very useful in the future.
@client.command(aliases=['test'])
async def __huu(ctx, *, iDontThingThisIsTooStrict):
    same = 'No idea but I just learned something.'
    await ctx.send(f'Question: {iDontThingThisIsTooStrict}\nAnswer: {same}')


#A command that clears a specified number of past messages (plus the command to clear). Default 5 messages.
@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount+1)


#Kick ban and unban functions.
@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')

@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.slpit('#')

    for ban_entry in banned_users:
        user=ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return


#Cog loader, reloader and unloader. Used to make changes to the bot on the fly while it is running via cogs.

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'The {extension} cog has been loaded!')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'The {extension} cog has been unloaded!')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'The {extension} cog has been reloaded!')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


#Background tasks that loop without imput.

@tasks.loop(hours=24)
async def change_status():
    random.shuffle(status)     #this shuffles the status list as soon as the on_ready triggers.
    iter_status = iter(status)  #turns the newly shuffeled 'status' into an iter.
    await client.change_presence(status=discord.Status(next(cycle_status)), activity= discord.Game(next(iter_status)))



client.run('Nzk5MDA4MDcwOTYwNDE0NzYx.X_9UQA.15bN7zV9Wt2YHT_eNiEsyniHIoA')
