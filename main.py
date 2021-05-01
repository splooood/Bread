import discord
from discord.ext import commands
import random
import time
from keep_alive import keep_alive
import random

client = commands.Bot(command_prefix = '?')

hexcode = ['0x0000FF', '0xFF0000', '0x00ff00']

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="prefix is '?'"))
  print('Your test bot is up and running.')

@client.command()
async def ping(ctx):
  await ctx.send(f'Pong! \nBot ping is {round(client.latency * 1000)} ms')

@client.command(aliases=['8ball', 'test'])
async def _8ball(ctx, *, question):
  responses = [
  "It is certain.",
  "It is decidedly so.",
  "Without a doubt.",
  "Yes - definitely.",
  "You may rely on it.",
  "As I see it, yes.",
  "Most likely.",
  "Outlook good.",
  "Yes.",
  "Signs point to yes.",
  "Reply hazy, try again.",
  "Ask again later.",
  "Better not tell you now.",
  "Cannot predict now.",
  "Concentrate and ask again.",
  "Don't count on it.",
  "My reply is no.",
  "My sources say no.",
  "Outlook not so good.",
  "Very doubtful."]
  await ctx.send(f'Your question was: {question}, \nMy answer is: {random.choice(responses)}')

@client.command()
async def purge(ctx, amount=5):
  if (ctx.message.author.permissions_in(ctx.message.channel).manage_messages):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'{amount} messages purged.')
    time.sleep(5)
    await ctx.channel.purge(limit=1)
  else:
    await ctx.send('Insufficient permissions: manage_messages')

@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
  if (ctx.message.author.permissions_in(ctx.message.channel).kick_members):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} has been kicked from the server.')
  else:
    await ctx.send('Insufficient permissions: kick_members')

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
  if (ctx.message.author.permissions_in(ctx.message.channel).ban_members):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} has been banned from the server.')
  else:
    await ctx.send('Insufficient permissions: ban_members')

@client.command()
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split('#')

  for ban_entry in banned_users:
    user = ban_entry.user
    
    if (user.name, user.discriminator) == (member_name, member_discriminator):
      if (ctx.message.author.permissions_in(ctx.message.channel).unban_members):
        await ctx.guild.unban(user)
        await ctx.send(f'Unbanned {user.mention} from server.')
      return
    return

@client.command()
async def warn(ctx, user: discord.User, *, message=None):
    message = message or "You have been warned. \nReason: None specified"
    await user.send(f'You have been warned. \nReason: {message}')

keep_alive()
client.run ('TOKEN')