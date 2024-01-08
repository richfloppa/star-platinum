import discord
from discord.ext import commands
import os
import asyncio
from keep_alive import keep_alive
keep_alive()


intents = discord.Intents.all()

bot = commands.Bot(command_prefix=['s!', 'S!'], intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await update_status()

async def update_status():
    ora_phrases = ["Ora!", "Ora! Ora!", "Ora! Ora! Ora!"]

    while True:
        for phrase in ora_phrases:
            await bot.change_presence(activity=discord.Game(name=phrase))
            await asyncio.sleep(3)

@bot.event
async def on_message(message):
    if message.author.bot:  # Check if the author of the message is a bot
        return

    if message.channel.id == 1171057744166522973:
        if not message.content.lower().endswith(" ora"):
            warn_message = await message.channel.send(f"{message.author.mention} **Your message does not end with** `ora`**.**  **EX:** ```Hello there! Ora```")
            await message.delete()
            await asyncio.sleep(3)
            await warn_message.delete()

    await bot.process_commands(message)

@bot.command(name='clear', help='Clear a specified number of messages')
async def clear(ctx, amount=5):
    # Check if the user has the manage_messages permission
    if ctx.message.author.guild_permissions.manage_messages:
        # Delete the specified number of messages plus the command itself
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'{amount} messages cleared by {ctx.message.author.mention}.', delete_after=5)
    else:
        await ctx.send('You do not have the manage_messages permission.')


@bot.event
async def on_disconnect():
    print("Bot disconnected. Reconnecting...")

@bot.event
async def on_error(event, *args, **kwargs):
    print(f"Error in {event}: {args[0]}")
    if isinstance(args[0], discord.ConnectionClosed):
        print("Reconnecting...")
        await asyncio.sleep(5)  # Add a delay before attempting to reconnect
        await bot.login(token, bot=True)
        await bot.connect()

token = os.getenv("token")

if token is None:
    print("Error: Token not found in environment variables.")
else:
    bot.run(token)
