import discord
from discord.ext import commands
import asyncio
embed_color = 0x36393f


class Choose_Country(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji='🇰🇿', custom_id='persistent_view:kz')
    async def kz(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed_question = discord.Embed(title=f'{interaction.user.name}, вы успешно выбрали 🇰🇿!',
                                       description='Вам был выдан доступ к остальным каналам.', color=embed_color)
        embed_question.set_thumbnail(url=interaction.user.avatar)
        role = interaction.guild.get_role(1122545297659265165)
        await interaction.user.add_roles(role)
        await interaction.user.send(interaction.user.mention, embed=embed_question)

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji='🇷🇺', custom_id='persistent_view:ru')
    async def ru(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed_question = discord.Embed(title=f'{interaction.user.name}, вы успешно выбрали 🇷🇺!',
                                       description='Вам был выдан доступ к остальным каналам.', color=embed_color)
        embed_question.set_thumbnail(url=interaction.user.avatar)
        role = interaction.guild.get_role(1122544664948527317)
        await interaction.user.add_roles(role)
        await interaction.user.send(interaction.user.mention, embed=embed_question)

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji='🇧🇾', custom_id='persistent_view:by')
    async def by(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed_question = discord.Embed(title=f'{interaction.user.name}, вы успешно выбрали 🇧🇾!',
                                       description='Вам был выдан доступ к остальным каналам.', color=embed_color)
        embed_question.set_thumbnail(url=interaction.user.avatar)
        role = interaction.guild.get_role(1122545259151360020)
        await interaction.user.add_roles(role)
        await interaction.user.send(interaction.user.mention, embed=embed_question)

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji='🇺🇦', custom_id='persistent_view:ua')
    async def ua(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed_question = discord.Embed(title=f'{interaction.user.name}, вы успешно выбрали 🇺🇦!',
                                       description='Вам был выдан доступ к остальным каналам.', color=embed_color)
        embed_question.set_thumbnail(url=interaction.user.avatar)
        role = interaction.guild.get_role(1122545301262192682)
        await interaction.user.add_roles(role)
        await interaction.user.send(interaction.user.mention, embed=embed_question)

class country_choose(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        bot.add_view(Choose_Country())

    @commands.has_any_role(1122550135340150806)
    @commands.command()
    async def send(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Выбор страны",
                              description="Чтобы получить доступ к остальным каналам, выберите страну в которой вы родились",
                              color=embed_color)
        await interaction.channel.send(embed=embed, view=Choose_Country())

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(country_choose(bot),guild=discord.Object(id=1038811883530108938))