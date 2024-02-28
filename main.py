from utils.jokes_api import get_jokes
from discord.ext import commands
import discord
from dotenv import load_dotenv
from config import BOT_TOKEN, GENERAL_CHANNEL_ID
import logging
import os

if os.path.exists('log.txt'):
    with open('log.txt', 'r+') as f:
        f.truncate(0)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler(
                        'log.txt'), logging.StreamHandler()],
                    level=logging.INFO)



load_dotenv('config.env')

LOGGER = logging.getLogger(__name__)


if(len(BOT_TOKEN) == 0):
    LOGGER.error("BOT TOKEN Missing")
    exit(1)


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!',
                   intents=intents)

@bot.event
async def on_ready():
    print(f'Ready as {bot.user.display_name}')
    LOGGER.info(f"Ready as {bot.user.display_name}")

@bot.event
async def on_member_join(member):
    if GENERAL_CHANNEL_ID is None:
        LOGGER.error("GENERAL CHANNEL ID MISSING")
    else:
        id = int(GENERAL_CHANNEL_ID)
        channel = bot.get_channel(id)
        mes:str = await get_jokes()
        await channel.send(mes)


@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello I am {bot.user.display_name}')


bot.run(BOT_TOKEN)
