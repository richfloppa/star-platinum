import discord
from discord.ext import commands, tasks
import itertools
import asyncio
import os
import requests
import openai
from keep_alive import keep_alive
keep_alive()


intents = discord.Intents.all()

# Set your OpenAI API key
openai.api_key = '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'

your_mom_jokes = [
    "Your mom is so fat, when she steps on the scale, it says 'to be continued.'",
    "Your mom is so old, she knew Burger King while he was still a prince.",
    "Your mom is so kind, she brought a spoon to the super bowl.",
    # Add more jokes to the list
]

bot = commands.Bot(command_prefix='?', intents=intents)

status_messages = itertools.cycle(["Real blue smurf cat, no cap", "Merry Christmas!"])

@bot.event
async def on_ready():
    change_status.start()
    print(f'Logged in as {bot.user.name}')

@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=discord.Game(name=next(status_messages)))

@bot.command(name='clear', help='Clears a specified number of messages')
async def clear(ctx, amount: int):
    # Delete the command message
    await ctx.message.delete()

    try:
        # Purge messages
        deleted_messages = await ctx.channel.purge(limit=amount)

        # Create an embed
        embed = discord.Embed(
            title='Messages Cleared',
            description=f'Successfully deleted {len(deleted_messages)} messages.',
            color=discord.Color.green()
        )

        # Set the bot's avatar as the thumbnail
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/1008001884738560051/118667056381.webp?ex=65941815&is=6581a315&hm=c73f8800ea6139aab596dafa40bd8f83997c18abc91b50c0f4e87ee1bef4710b&=&format=webp')

        # Send the embed message
        await ctx.send(embed=embed)

    except discord.Forbidden:
        # If the bot doesn't have permission to delete messages or send messages, handle the error
        await ctx.send("Error: I don't have permission to delete messsages.")

    except discord.HTTPException as e:
        # If an HTTP error occurs (e.g., messages are too old), handle the error
        await ctx.send(f"**Make sure you are using command as:** `?clear <number of message>`")

@bot.command(name='joke', help='Get a joke')
async def yourmom(ctx):
    # Fetch a "your mom" joke from the icanhazdadjoke API
    api_url = 'https://icanhazdadjoke.com/'
    headers = {'Accept': 'application/json'}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        # Extract the joke from the response
        joke = response.json()['joke']

        # Send the joke to the chat
        await ctx.send(joke)
    else:
        await ctx.send('Error: Unable to fetch a joke.')

@bot.command(name='yourmom', help='Get a "your mom" joke')
async def yourmom(ctx):
    # Fetch a "your mom" joke from the yomomma.info API
    api_url = 'https://api.yomomma.info/'
    response = requests.get(api_url)

    if response.status_code == 200:
        # Extract the joke from the response
        joke = response.json()['joke']

        # Send the joke to the chat
        await ctx.send(joke)
    else:
        await ctx.send('Error: Unable to fetch a "your mom" joke.')

@bot.event
async def on_disconnect():
    print("Bot disconnected. Reconnecting...")
    await asyncio.sleep(5)  # Add a delay before attempting to reconnect
    await bot.login(token, bot=True)
    await bot.connect()

token = os.getenv("token")

if token is None:
    print("Error: Token not found in environment variables.")
else:
    bot.run(token)
