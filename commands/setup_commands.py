import discord
from discord.ext import commands
from discord import app_commands
from sqlalchemy import create_engine, select, and_
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship
from database_init import User, RegisteredPlayers
from datetime import date
import datetime
import config

class SetupCommands(commands.GroupCog, name="setup"):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="new_player", description="Add a new player to participate.")
    async def new_player(self, interaction: discord.Interaction):
        player = interaction.user.id
        engine = create_engine(config.db_path)

        with Session(engine) as session:
            stmt = select(User).where(User.discord_id == player)
            user = session.scalars(stmt).all()

            if user:
                await interaction.response.send_message("You are already registered with the bot!", ephemeral=True)
            else:
                new_user = User(discord_id=player)
                first_channel = RegisteredPlayers(guild_id=interaction.guild.id, user_id=player)
                session.add_all([new_user, first_channel])
                session.commit()
                session.close()
                await interaction.response.send_message("You are now registered to play!"
                                                        "\n Try '/help info' to get started.", ephemeral=True)

    @app_commands.command(name="leaderboard_register", description="Add yourself to the leaderboard of another server.")
    async def leaderboard_register(self, interaction: discord.Interaction):
        player = interaction.user.id
        server = interaction.guild.id
        engine = create_engine(config.db_path)

        with Session(engine) as session:

            if not session.scalars(select(User).where((User.discord_id)==player)).all():
                await interaction.response.send_message("Please register with the bot first. '/setup new_player'.", ephemeral=True)
            else:
                stmt = select(RegisteredPlayers).where(and_(RegisteredPlayers.user_id == player), (RegisteredPlayers.guild_id == server))
                user = session.scalars(stmt).all()
                if user:
                    await interaction.response.send_message("You are already registered on this server.", ephemeral=True)
                else:
                    leaderboard = RegisteredPlayers(guild_id=server, user_id=player)
                    session.add_all([leaderboard])
                    session.commit()
                    session.close()
                    await interaction.response.send_message("You are now registered with the leaderboard on this server!", ephemeral=True)