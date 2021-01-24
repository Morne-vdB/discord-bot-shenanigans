import discord
from discord.ext import commands

class Example(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        #await self.client.change_presence(status=discord.Status.invisible, activity=discord.Game('.help'))
        print('Bot is online.')

    @commands.command()
    async def ding(self, ctx):
        await ctx.send(f'Dong {round(self.client.latency * 1000)}ms')

def setup(client):
    client.add_cog(Example(client))
