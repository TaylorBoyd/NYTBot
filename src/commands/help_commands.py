import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button

class HelpCommands(commands.GroupCog, name="help"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="info", description="Information about the NYT bot.")
    async def info(self, interaction: discord.Interaction):
        response = ("This bot is set up to record stats for 4 different New York Times minigames! Play and submit your scores once a day, leaderboards coming soon."
                    "\n> [Wordle](https://www.nytimes.com/games/wordle/index.html) - try to get the lowest number of guesses"
                    "\n> [Connections](https://www.nytimes.com/games/connections) - try to get all of the connections with out losing any lives"
                    "\n> [Strands](https://www.nytimes.com/games/strands) - find all of the words with no hints"
                    "\n> [Crossword Mini](https://www.nytimes.com/crosswords/game/mini) - complete this in the fastest time")
        view = View()
        button = Button(label="Submit Scores", style=discord.ButtonStyle.primary, custom_id="submit_scores")
        view.add_item(button)
        await interaction.response.send_message(response, suppress_embeds=True, view=view)

    @app_commands.command(name="setup", description="Explains the setup process to get the bot going in your channel.")
    async def setup(self, interaction: discord.Interaction):
        msg = ('> Begin with using the command "/setup new_player" in the main channel. This will register you with the bot and that servers leaderboards'
               '\n> If you would like to register on a leaderboard in another server, use the "/setup leaderboard_register" command in that server')
        await interaction.response.send_message(msg)

    @app_commands.command(name="scoring", description="Explains how the scoring system works.")
    async def scoring(self, interaction: discord.Interaction):
        msg = ('Try to score as many points as possible each day! 30 points is the maximum possible and daily '
               'tiebreaks are done by fastest mini time.'
               '\n> Wordle: One point lost for each guess. Maximum of 6 points at first guess.'
               '\n> Connections: No mistakes = 8 points. One point lost for each incorrect guess and missed connection.'
               '\n> Strands: Zero hints = 8 points, one point lost for each hint used.'
               '\n> Crossword Mini: Under 1:00 is 8 points, under 2:00 is 7 points, under 3:00 is 6 points, '
               'etc...Cannot go below zero')
        await interaction.response.send_message(msg, ephemeral=True)

    #@app_commands.command(name="test1", description="test process")
    #async def test1(self, interaction: discord.Interaction):
    #    channel = self.bot.get_channel(1274399471723348030)
    #    await channel.send("Test01")
    #    await interaction.response.send_message("finished")

