import discord
from discord.ui import Button, View
import datetime
from sqlalchemy import create_engine, select, and_
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship
from database_init import User, RegisteredPlayers, NYT_scores
from datetime import date
import config

class ScoreButtons(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, wordle, connections, conenction_lives, strands, mini_minutes, mini_seconds):
        super().__init__()
        self.wordle = wordle
        self.connections = connections
        self.connection_lives = conenction_lives
        self.strands = strands
        self.mini_minutes = mini_minutes
        self.mini_seconds = mini_seconds

        if self.wordle >= 7:
            self.remove_item(self.wordle_guesses)
        if self.connections >= 4:
            self.remove_item(self.connections_made)
        if self.connection_lives < 1:
            self.remove_item(self.connections_left)
        if self.mini_seconds >= 50:
            self.remove_item(self.mini_seconds_10)
        if self.mini_seconds >= 59:
            self.remove_item(self.mini_seconds_10)
            self.remove_item(self.mini_seconds_1)

    @discord.ui.button(label="Wordle Guesses", style=discord.ButtonStyle.success)
    async def wordle_guesses(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.wordle += 1
        view = ScoreButtons(interaction, self.wordle, self.connections, self.connection_lives, self.strands,
                            self.mini_minutes, self.mini_seconds)
        if self.mini_seconds < 10:
            mini_time = f"{self.mini_minutes}:0{self.mini_seconds}"
        else:
            mini_time = f"{self.mini_minutes}:{self.mini_seconds}"
        await interaction.response.edit_message(content="> Submit your scores now!"
                                                        f"\n> Wordle Guesses: {self.wordle}"
                                                        f"\n> Connections Made: {self.connections}"
                                                        f"\n> Connections Lives: {self.connection_lives}"
                                                        f"\n> Strands Hints Used: {self.strands}"
                                                        f"\n> Mini Time: {mini_time}", view=view)

    @discord.ui.button(label="Connections Made", style=discord.ButtonStyle.success)
    async def connections_made(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.connections += 1
        view = ScoreButtons(interaction, self.wordle, self.connections, self.connection_lives, self.strands,
                            self.mini_minutes, self.mini_seconds)
        if self.mini_seconds < 10:
            mini_time = f"{self.mini_minutes}:0{self.mini_seconds}"
        else:
            mini_time = f"{self.mini_minutes}:{self.mini_seconds}"
        await interaction.response.edit_message(content="> Submit your scores now!"
                                                        f"\n> Wordle Guesses: {self.wordle}"
                                                        f"\n> Connections Made: {self.connections}"
                                                        f"\n> Connections Lives: {self.connection_lives}"
                                                        f"\n> Strands Hints Used: {self.strands}"
                                                        f"\n> Mini Time: {mini_time}", view=view)

    @discord.ui.button(label="Connection Lives (-1)", style=discord.ButtonStyle.primary)
    async def connections_left(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.connection_lives -= 1
        view = ScoreButtons(interaction, self.wordle, self.connections, self.connection_lives, self.strands,
                            self.mini_minutes, self.mini_seconds)
        if self.mini_seconds < 10:
            mini_time = f"{self.mini_minutes}:0{self.mini_seconds}"
        else:
            mini_time = f"{self.mini_minutes}:{self.mini_seconds}"
        await interaction.response.edit_message(content="> Submit your scores now!"
                                                        f"\n> Wordle Guesses: {self.wordle}"
                                                        f"\n> Connections Made: {self.connections}"
                                                        f"\n> Connections Lives: {self.connection_lives}"
                                                        f"\n> Strands Hints Used: {self.strands}"
                                                        f"\n> Mini Time: {mini_time}", view=view)

    @discord.ui.button(label="Strands Hints", style=discord.ButtonStyle.success)
    async def strands_hints(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.strands += 1
        view = ScoreButtons(interaction, self.wordle, self.connections, self.connection_lives, self.strands,
                            self.mini_minutes, self.mini_seconds)
        if self.mini_seconds < 10:
            mini_time = f"{self.mini_minutes}:0{self.mini_seconds}"
        else:
            mini_time = f"{self.mini_minutes}:{self.mini_seconds}"
        await interaction.response.edit_message(content="> Submit your scores now!"
                                                        f"\n> Wordle Guesses: {self.wordle}"
                                                        f"\n> Connections Made: {self.connections}"
                                                        f"\n> Connections Lives: {self.connection_lives}"
                                                        f"\n> Strands Hints Used: {self.strands}"
                                                        f"\n> Mini Time: {mini_time}", view=view)

    @discord.ui.button(label="Mini Minutes", style=discord.ButtonStyle.success)
    async def mini_minutes_1(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.mini_minutes += 1
        view = ScoreButtons(interaction, self.wordle, self.connections, self.connection_lives, self.strands,
                            self.mini_minutes, self.mini_seconds)
        if self.mini_seconds < 10:
            mini_time = f"{self.mini_minutes}:0{self.mini_seconds}"
        else:
            mini_time = f"{self.mini_minutes}:{self.mini_seconds}"
        await interaction.response.edit_message(content="> Submit your scores now!"
                                                        f"\n> Wordle Guesses: {self.wordle}"
                                                        f"\n> Connections Made: {self.connections}"
                                                        f"\n> Connections Lives: {self.connection_lives}"
                                                        f"\n> Strands Hints Used: {self.strands}"
                                                        f"\n> Mini Time: {mini_time}", view=view)

    @discord.ui.button(label="Mini Seconds (10)", style=discord.ButtonStyle.success)
    async def mini_seconds_10(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.mini_seconds += 10
        view = ScoreButtons(interaction, self.wordle, self.connections, self.connection_lives, self.strands,
                            self.mini_minutes, self.mini_seconds)
        if self.mini_seconds < 10:
            mini_time = f"{self.mini_minutes}:0{self.mini_seconds}"
        else:
            mini_time = f"{self.mini_minutes}:{self.mini_seconds}"
        await interaction.response.edit_message(content="> Submit your scores now!"
                                                        f"\n> Wordle Guesses: {self.wordle}"
                                                        f"\n> Connections Made: {self.connections}"
                                                        f"\n> Connections Lives: {self.connection_lives}"
                                                        f"\n> Strands Hints Used: {self.strands}"
                                                        f"\n> Mini Time: {mini_time}", view=view)

    @discord.ui.button(label="Mini Seconds (1)", style=discord.ButtonStyle.success)
    async def mini_seconds_1(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.mini_seconds += 1
        view = ScoreButtons(interaction, self.wordle, self.connections, self.connection_lives, self.strands,
                            self.mini_minutes, self.mini_seconds)
        if self.mini_seconds < 10:
            mini_time = f"{self.mini_minutes}:0{self.mini_seconds}"
        else:
            mini_time = f"{self.mini_minutes}:{self.mini_seconds}"
        await interaction.response.edit_message(content="> Submit your scores now!"
                                                        f"\n> Wordle Guesses: {self.wordle}"
                                                        f"\n> Connections Made: {self.connections}"
                                                        f"\n> Connections Lives: {self.connection_lives}"
                                                        f"\n> Strands Hints Used: {self.strands}"
                                                        f"\n> Mini Time: {mini_time}", view=view)

    @discord.ui.button(label="Finish", style=discord.ButtonStyle.danger)
    async def finish(self, interaction: discord.Interaction, button: discord.ui.Button):
        player = interaction.user.id
        engine = create_engine(config.db_path)
        with Session(engine) as session:
            if session.scalars(select(NYT_scores).where(and_(NYT_scores.user_id == player), (NYT_scores.date) == date.today())).all():
                await interaction.response.send_message("You have already submitted your scores for today.", ephemeral=True)
            else:
                mini_time = (self.mini_minutes * 60) + (self.mini_seconds)
                connections_score = (self.connections + (-4 + self.connection_lives))
                scores = NYT_scores(wordle_score=self.wordle,
                                    connections_score = connections_score,
                                    strands_score = self.strands,
                                    mini_time = mini_time,
                                    date=date.today(),
                                    user_id=player)
                session.add_all([scores])
                session.commit()
        await interaction.response.send_message(f"{interaction.user.mention}, your scores are submitted!", ephemeral=True)

    @discord.ui.button(label="Reset", style=discord.ButtonStyle.danger)
    async def reset(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = ScoreButtons(interaction, 0,0,4,0,0,0)
        await interaction.response.edit_message(content="> Submit your scores now!"
                                                        f"\n> Wordle Guesses: 0"
                                                        f"\n> Connections Made: 0"
                                                        f"\n> Connections Lives: 4"
                                                        f"\n> Strands Hints Used: 0"
                                                        f"\n> Mini Time: 00:00", view=view)