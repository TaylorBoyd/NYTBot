import discord
from discord.ext import commands
from discord import app_commands
from sqlalchemy import create_engine, select, and_
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship
from database_init import User, RegisteredPlayers
from datetime import date
from typing import Optional
from helpers.ScoreHelper import ScoreHelper
import datetime
import config

class StatsCommands(commands.GroupCog, name="stats"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="server_daily_leaderboard", description="Check the daily winner for this server. Choose "
                                                                  "which day. "
                                                           "Choose which day or leave blank to see today's "
                                                           "leaderboard.")
    async def server_daily_leaderboard(self, interaction: discord.Interaction,
                           month: int, day: int, year: Optional[int]):
        """
        :param month: 1-12 to pick the month
        :param day: Pick which day you want to check the leaderboard
        :param year: Optional, default choice is this year
        """
        server = interaction.guild.id
        score_month = month
        score_day = day
        if not year:
            score_year = datetime.date.today().year
        else:
            score_year = year

        try:
            score_date = date(score_year, score_month, score_day)
        except ValueError:
            await interaction.response.send_message("That is not a valid date.", ephemeral=True)
            return

        players = ScoreHelper.get_server_players(server)
        scores = ScoreHelper.get_server_daily(players, score_date)
        msg = ""
        pass