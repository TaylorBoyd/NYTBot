import discord
from discord.ext import commands
from sqlalchemy import create_engine, select, and_
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship
from database_init import User, RegisteredPlayers, NYT_scores
from datetime import date
from buttons.ScoreButtons import ScoreButtons
import datetime
import config

class ButtonListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type == discord.InteractionType.component:
            player = interaction.user.id
            custom_id = interaction.data["custom_id"]
            engine = create_engine(config.db_path)


            if custom_id == "submit_scores":
                with Session(engine) as session:

                    if not session.scalars(select(User).where((User.discord_id) == player)).all():
                        await interaction.response.send_message("Please register with the bot first. '/setup new_player'.", ephemeral=True)
                    else:
                        if session.scalars(select(NYT_scores).where(and_(NYT_scores.user_id == player), (NYT_scores.date) == date.today())).all():
                            await interaction.response.send_message("You have already submitted your scores for today.", ephemeral=True)
                        else:
                            view = ScoreButtons(interaction, 0, 0, 4, 0, 0, 0)
                            await interaction.response.send_message("> Submit your scores now!"
                                                                    f"\n> Wordle Guesses: 0"
                                                                    f"\n> Connections Made: 0"
                                                                    f"\n> Connections Lives: 4"
                                                                    f"\n> Strands Hints Used: 0"
                                                                    f"\n> Mini Time: 00:00", ephemeral=True, view=view)