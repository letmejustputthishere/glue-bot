from discord.ext import commands
from discord import Guild


class OnJoin(commands.Cog, name="dm server owner module"):
    """Cog that sends a message to person adding the bot to the server"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: Guild):
        # get the owner of a guild, this needs the "members" intent
        owner = guild.owner
        # send a message to the owner if it exists
        if owner:
            await owner.send(
                f"Hey there, thanks for having me 🥳\n"
                f"If you want to setup an NFT project to grant holder roles to members, run the `/setup` command in a channel of the respective server.\n"
                f"If you feel lost, you can always run `/help` to get and overview of what I can do 😊\n"
            )
