import os
import logging
import random
import platform

from utils.extra_functions import get_jokes
from discord.ext import commands, tasks
from discord.ext.commands import Context
import discord
from config import BOT_TOKEN, GENERAL_CHANNEL_ID


if os.path.exists('log.txt'):
    with open('log.txt', 'r+') as f:
        f.truncate(0)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO
)

LOGGER = logging.getLogger(__name__)


class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            help_command=None,
            intents=intents,
        )

    async def load_cogs(self) -> None:
        for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    self.load_extension(f"cogs.{extension}")
                    LOGGER.info(f"Loaded extension '{extension}'")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    LOGGER.error(
                        f"Failed to load extension {extension}\n{exception}"
                    )

    @tasks.loop(minutes=1.0)
    async def status_task(self) -> None:
        """
        Setup the game status task of the bot.
        """
        statuses = ["Pretending that I know Everything", "Bullying the kids",
                    "Who knows"]
        await self.change_presence(activity=discord.Game(random.choice(statuses)))

    @status_task.before_loop
    async def before_status_task(self) -> None:
        """
        Before starting the status changing task, we make sure the bot is ready
        """
        await self.wait_until_ready()

    async def on_ready(self):
        LOGGER.info(f"Ready as {self.user.display_name}")
        LOGGER.info(f"py-cord version: {discord.__version__}")
        LOGGER.info(f"Python Version: {platform.python_version()}")
        LOGGER.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
        LOGGER.info("-----------------------------------------")

        await self.load_cogs()
        self.status_task.start()

    async def on_command_error(self, context: Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.NotOwner):
            embed = discord.Embed(description="Err, You are not the Bot Owner", color=0xE02B2B)
            await context.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description="You are missing the permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` to execute this command!",
                color=0xE02B2B,
            )
            await context.send(embed=embed)

        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                description="I am missing the permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` to fully perform this command!",
                color=0xE02B2B,
            )
            await context.send(embed=embed)

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Error!",
                description=str(error).capitalize(),
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        else:
            raise error

    async def on_member_join(self, member):
        if GENERAL_CHANNEL_ID is None:
            LOGGER.error("GENERAL CHANNEL ID MISSING")
            return
        try:
            id = int(GENERAL_CHANNEL_ID)
            channel = self.get_channel(id)
            success, joke = await get_jokes()
            mes = "Welcome to the server."
            if success:
                mes = f"Welcome to the server.\nHere is a Joke for you:\n{joke}"
            await channel.send(mes)
        except Exception:
            LOGGER.error("Error Sending Welcome Message")


bot = DiscordBot()
bot.run(BOT_TOKEN)
