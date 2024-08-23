import discord
import config
from discord.ext import commands
from commands.help_commands import HelpCommands
from commands.setup_commands import SetupCommands
from listener.ButtonListener import ButtonListener
from helpers.ScoreHelper import ScoreHelper


bot = commands.Bot(command_prefix="$", intents=discord.Intents.default())

@bot.event
async def on_ready():
    await bot.add_cog(HelpCommands(bot))
    await bot.add_cog(SetupCommands(bot))
    await bot.add_cog(ButtonListener(bot))
    await bot.tree.sync()
    print("Bot is now ready")

bot.run(config.token)


