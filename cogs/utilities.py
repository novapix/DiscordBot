# import json
import httpx

import discord
from discord.ext import commands
from discord.ext.commands import Context

from config import OPENWEATHERMAPAPI as app_id


class Utilities(commands.Cog, name="utilities"):
    def __init__(self, bot) -> None:
        self.bot = bot

    def kelvin_to_celsius(self, kelvin):
        """Converts a temperature from Kelvin to Celsius.

        :param kelvin: The temperature in Kelvin.
        Returns: The temperature in Celsius.
        """
        celsius = kelvin - 273.15
        return round(celsius, 3)

    @commands.command(
        name="weather",
        description="Get weather of a location",
    )
    async def send_weather(self, context: Context, *, location: str = None):
        """
        Gets and Send Weather details

        :param context: The command context
        :param location: Location which weather is to be fetched
        """
        if not app_id:
            embed = discord.Embed(
                description="API KEY NOT PROVIDED",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return

        if not location:
            embed = discord.Embed(
                description="Location argument Missing",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return
        # location = urllib.par
        msg = await context.send("Trying to get Weather")
        url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={app_id}'
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url=url, timeout=20.0)
            except httpx.TimeoutException:
                await msg.edit("Timeout Error")
                return

            if response.status_code != 200:
                await msg.edit("Failed to Get Weather")
                return

            result = response.json()
            try:
                cityname = result['name']
                curtemp = result['main']['temp']
                humidity = result['main']['humidity']
                min_temp = result['main']['temp_min']
                max_temp = result['main']['temp_max']
                desc = result['weather'][0]
                desc = desc['main']

            except KeyError:
                await msg.edit("Error Occured")
                return

            await msg.edit(
                f"`{cityname} weather` \n" +
                f"**Temperature:** `{self.kelvin_to_celsius(curtemp)}°C` \n" +
                f"**Min. Temp.:** `{self.kelvin_to_celsius(min_temp)}°C` \n" +
                f"**Max. Temp.:** `{self.kelvin_to_celsius(max_temp)}°C` \n" +
                f"**Humidity:** `{humidity}%`\n"
            )


def setup(bot) -> None:
    bot.add_cog(Utilities(bot))
