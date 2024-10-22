import discord
from discord.ext import commands
from discord import app_commands
import datetime
from sqlalchemy import create_engine, select, and_, delete
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship
from database_init import User, RegisteredPlayers, NYT_scores
from datetime import date, datetime, timedelta
from typing import Optional
from helpers.ScoreHelper import ScoreHelper
import config

class StatsCommands(commands.GroupCog, name="stats"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="server_daily_leaderboard", description="Check the daily winner for this server.")
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
            score_year = datetime.today().year
        else:
            score_year = year

        try:
            score_date = date(score_year, score_month, score_day)
        except ValueError:
            await interaction.response.send_message("That is not a valid date.", ephemeral=True)
            return
        await interaction.response.defer(thinking=True)
        players = ScoreHelper.get_server_players(server)
        scores = ScoreHelper.get_server_daily(players, score_date)
        if not scores:
            await interaction.followup.send(f"There are no scores for {score_date} on this server")
            return
        msg = f"Winners for {score_date}!"
        place = 1
        while place < 11:
            if not scores:
                await interaction.followup.send(msg)
                return
            player = scores.pop(0)
            msg += f"\n> {place}. <@{player[0]}> with {player[1]} points and a mini time of {player[2]} seconds."
            place += 1
        await interaction.followup.send(msg)

    @app_commands.command(name="submit", description="Submit a score for today.")
    async def submit(self, interaction: discord.Interaction, wordle: int, connections: int, connection_lives: int,
                     strands: int, mini: int):
        """
        :param wordle: Input the number of wordle guesses. 7 means you did not guess the word
        :param connections: Number of connections made
        :param connection_lives: How many connections mistakes do you have left?
        :param strands: How many hints did you use for strands?
        :param mini: How many seconds did it take to complete the mini?
        """
        player = interaction.user.id
        fixed_time = (datetime.today() - timedelta(hours=4))
        engine = create_engine(config.db_path)

        """
        Preventing impossible inputs first.
        """
        if wordle < 1 or wordle > 7:
            await interaction.response.send_message("You input an invalid wordle score. It must be between 1 and 7", ephemeral=True)
            return
        if connections < 0 or connections > 4:
            await interaction.response.send_message("You input an invalid connections score. It must be between 0 and 4",
                                                    ephemeral=True)
            return
        if connection_lives < 0 or connection_lives > 4:
            await interaction.response.send_message(
                "You input an invalid connections lives score. It must be between 0 and 4",
                ephemeral=True)
            return
        if strands < 0:
            await interaction.response.send_message(
                "Hints for strands must be greater than zero.",
                ephemeral=True)
            return
        if mini <= 0:
            await interaction.response.send_message(
                "Scores for the mini cannot be negative. Please input how many seconds it took to complete.",
                ephemeral=True)
            return

        with Session(engine) as session:
            if session.scalars(select(NYT_scores).where(and_(NYT_scores.user_id == player), (NYT_scores.date) == fixed_time.date())).all():
                await interaction.response.send_message("You have already submitted your scores for today.",
                                                        ephemeral=True)
            else:
                connections_score = (connections + (-4 + connection_lives))
                daily_score = ScoreHelper.generate_score(wordle, connections_score, strands, int((mini / 60)))
                scores = NYT_scores(wordle_score=wordle,
                                    connections_score=connections_score,
                                    strands_score=strands,
                                    mini_time=mini,
                                    date=fixed_time.date(),
                                    user_id=player,
                                    daily_score=daily_score)
                session.add_all([scores])
                session.commit()
        await interaction.response.send_message(f"{interaction.user.mention}, your scores are submitted! Today's "
                                                f"score was {daily_score}",
                                                ephemeral=True, delete_after=180)

    @app_commands.command(name="delete", description="Delete your score for today. Useful if you've made a mistake entering.")
    async def delete(self, interaction: discord.Interaction):
        player = interaction.user.id
        fixed_time = (datetime.today() - timedelta(hours=4))
        engine = create_engine(config.db_path)
        with Session(engine) as session:
            if session.scalars(select(NYT_scores).where(and_(NYT_scores.user_id == player),(NYT_scores.date) == fixed_time.date())).all():
                del1 = delete(NYT_scores).where(and_((NYT_scores.user_id == player),(NYT_scores.date) ==
                                                  fixed_time.date()))
                session.execute(del1)
                session.commit()
                await interaction.response.send_message("Today's scores are deleted.",
                                                        ephemeral=True)
            else:
                await interaction.response.send_message("You have not submitted a score today!",
                                                        ephemeral=True)