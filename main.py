import discord
from discord.ext import commands
import random
import time
from keep_alive import keep_alive
import requests
from discord import Member

client = commands.Bot(command_prefix = '?')

client.remove_command('help')

ratherapi = ['Stay up for 24 hours and get paid $10,000\n or \nStay up for 72 hours and get paid $20,000?', 'Punch your mom in the face for $1,000,000\n or \nPunch your grandma in the face for $10,000,000?', 'Live infinitely\n or \nadd 100 years to your life expectancy?']

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
  await user.send(f'You have been warned. \nReason:{message}')
  await ctx.send(f'User has been warned for {message}')

@client.command()
async def prefix(ctx):
  await ctx.send("The prefix is '?'.")

@client.command()
async def add(ctx):
  embed=discord.Embed(title="Add Me", url = 'https://ja2711733.wixsite.com/gigbit',  description="Click the link above to add Gigabit to your server.", color=discord.Color.blue())
  embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed)

@client.command()
async def catpics(ctx):
  response = requests.get('https://api.thecatapi.com/v1/images/search')
  data = response.json()
  embed=discord.Embed(title="Your Requested Cat Pic! <:cat:840334556133589042>", description="Here's your cat pic.", color=discord.Color.blue())
  embed.set_image(url=data[0]['url'])
  await ctx.send(embed=embed)

@client.command()
async def dogpics(ctx):
  response = requests.get('https://dog.ceo/api/breeds/image/random')
  data = response.json()
  embed=discord.Embed(title="Your Requested Dog Pic! <:dog:840345472333119538>", description="Here's your dog pic.", color=discord.Color.blue())
  embed.set_image(url=data['message'])
  await ctx.send(embed=embed)

@client.command()
async def pfp(ctx, member: Member = None):
  if not member:
    member = ctx.author
  embed=discord.Embed(title="We went to infinity and beyond and...", description="We fetched the profile picture you wanted!", color=discord.Color.blue())
  embed.set_image(url=member.avatar_url)
  embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed)

@client.command()
async def rng(ctx):
    def check(msg):
        return msg.author == ctx.author and msg.content.isdigit() and \
               msg.channel == ctx.channel

    await ctx.send("Type your first number.")
    msg1 = await client.wait_for("message", check=check)
    await ctx.send("Type your second number (Must be bigger than the first).")
    msg2 = await client.wait_for("message", check=check)
    x = int(msg1.content)
    y = int(msg2.content)
    if x < y:
        value = random.randint(x,y)
        await ctx.send(f"Randomly generated a number: {value}.")
    else:
        await ctx.send(":warning: Please ensure the first number is smaller than the second number.")



@client.command()
async def help(ctx):
  embed=discord.Embed(title="Commands", description="Here are all of my commands.", color=discord.Color.blue())
  embed.add_field(name="Testing Commands", value="Test commands such as ping, alivecheck,etc.", inline=False)
  embed.add_field(name="``?ping``", value="Returns the ping of the bot.", inline=False)
  embed.add_field(name="``?prefix``", value="Returns the prefix of the bot.", inline=True)
  embed.add_field(name="``?add``", value="Returns with an embed containing an invite link for the bot.", inline=True)
  embed.add_field(name="Fun Commands", value="Fun commands such ass 8ball, RNG, catpics, etc.", inline=False)
  embed.add_field(name="``?rng``", value="Returns with a random number. You choose what number parameters you want.", inline=True)
  embed.add_field(name="``?8ball {question}``", value="Answers any question with a randomized answer.", inline=True)
  embed.add_field(name="``?catpics``", value="Returns with a randomized cat picture! (Aww.)")
  embed.add_field(name="``?dogpics``", value="Returns with a randomized cat picture! (Aww.)")
  embed.add_field(name="``?pfp {user}``", description="Fetched the specified user's profile picture and sends it. Default user set to messag author.", inline=True)
  embed.add_field(name="Basic Admin", value="Basic admin commands such as purge, kick, etc.", inline=False)
  embed.add_field(name="``?purge {amount}``", value="Deletes an amount of messages in a channel. Default amount set as '5'.", inline=True)
  embed.add_field(name="``?kick {user} {reason}``", value="Kicks a user. Must specify a reason. Default reason set to 'None'.", inline=True)
  embed.add_field(name="``?ban {user} {reason}``", value="Kicks a user. Must specify a reason. Default reason set to 'None'.", inline=True)
  embed.add_field(name="``?unban {user}``", value="Unbans user from guild. No reason needs to be specified.", inline=True)
  embed.add_field(name="``?warn {user} {reason}``", value="Warns a user via Direct Message. Reason needs to be specified. Default reason set to 'None'.", inline=True)
  embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
  embed.set_footer(text="Help command called by by: {}".format(ctx.author.display_name))
  await ctx.send(embed=embed)

keep_alive()
client.run ('tokemon, gotta catch em all! tokemon!')