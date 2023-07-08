from datetime import datetime

import discord
from discord import app_commands, ui
from discord.ext import commands
import asyncio
import sqlite3
embed_color = 0x36393f


class Request_Method(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji='✅', custom_id='persistent_view:request_yes')
    async def true(self, interaction: discord.Interaction, button: discord.ui.Button):
        message = interaction.message
        clicked = cursor.execute("SELECT clicked FROM requests WHERE message_id = {}".format(interaction.message.id)).fetchone()
        id = cursor.execute("SELECT id FROM requests WHERE message_id = {}".format(interaction.message.id)).fetchone()[0]
        quest1 = cursor.execute("SELECT quest1 FROM requests WHERE message_id = {}".format(interaction.message.id)).fetchone()[0]
        quest2 = cursor.execute("SELECT quest2 FROM requests WHERE message_id = {}".format(interaction.message.id)).fetchone()[0]
        quest3 = cursor.execute("SELECT quest3 FROM requests WHERE message_id = {}".format(interaction.message.id)).fetchone()[0]
        quest4 = cursor.execute("SELECT quest4 FROM requests WHERE message_id = {}".format(interaction.message.id)).fetchone()[0]
        member = interaction.guild.get_member(id)
        otvet = cursor.execute("SELECT otvet FROM requests WHERE message_id = {}".format(interaction.message.id)).fetchone()[0]
        if otvet is not None:
            await interaction.response.send_message("Данную заявку ужу обработали!", ephemeral=True)
        else:
            embed = discord.Embed(title="Ваша заявка на вступление в город была успешна одобрена!", description="Чтобы получить квартиру в нашем городе, обратитесь к администрации города", color=embed_color)
            await member.send(embed=embed)
            role = interaction.guild.get_role(1038812520049291344)
            await member.add_roles(role)
            cursor.execute("UPDATE requests SET clicked = 1 WHERE message_id = {}".format(interaction.message.id))
            cursor.execute("UPDATE requests SET otvet = 1 WHERE message_id = {}".format(interaction.message.id))
            connection.commit()
            embed = discord.Embed(
                description=f"**{quest1}** *написал анкету на вступление в город* (discord - {interaction.guild.get_member(id).mention})!\n\n> *Заявка была принята пользователем {interaction.user.mention}*",
                timestamp=datetime.utcnow(),
                color=embed_color)
            embed.add_field(name="Расскажите о себе:", value=f"{quest2}", inline=False)
            embed.add_field(name="Кем вы готовы стать в городе:", value=f"{quest3}", inline=False)
            embed.add_field(name="Чем вы готовы помочь городу:", value=f"{quest4}", inline=False)
            await member.edit(nick=quest1)
            await interaction.message.edit(embed=embed)
            await interaction.response.send_message(f'Вы успешно приняли заявку игрока {member.mention}!',
                                                    ephemeral=True)


    @discord.ui.button(style=discord.ButtonStyle.gray, emoji='❌', custom_id='persistent_view:request_no')
    async def false(self, interaction: discord.Interaction, button: discord.ui.Button):
        message = interaction.message
        clicked = cursor.execute("SELECT clicked FROM requests WHERE message_id = {}".format(interaction.message.id)).fetchone()[0]
        id = cursor.execute("SELECT id FROM requests WHERE message_id = {}".format(interaction.message.id)).fetchone()[0]
        quest1 = cursor.execute("SELECT quest1 FROM requests WHERE message_id = {}".format(interaction.message.id)).fetchone()[0]
        quest2 = cursor.execute("SELECT quest2 FROM requests WHERE message_id = {}".format(interaction.message.id)).fetchone()[0]
        quest3 = cursor.execute("SELECT quest3 FROM requests WHERE message_id = {}".format(interaction.message.id)).fetchone()[0]
        quest4 = cursor.execute("SELECT quest4 FROM requests WHERE message_id = {}".format(interaction.message.id)).fetchone()[0]
        member = interaction.guild.get_member(id)
        otvet = cursor.execute("SELECT otvet FROM requests WHERE message_id = {}".format(interaction.message.id)).fetchone()[0]
        if otvet is not None:
            await interaction.response.send_message("Данную заявку ужу обработали!", ephemeral=True)
        else:
            await interaction.response.send_modal(Request_Reason(interaction.message.id))

class Request_Reason(ui.Modal, title='Отклонение заявки игрока'):
    reason = ui.TextInput(label='Почему вы хотите отклонить заявку игрока?')

    def __init__(self, message_id) -> None:
        super().__init__()
        self.message_id = message_id



    async def on_submit(self, interaction: discord.Interaction):
        message = interaction.message
        clicked = cursor.execute("SELECT clicked FROM requests WHERE message_id = {}".format(self.message_id)).fetchone()[0]
        id = cursor.execute("SELECT id FROM requests WHERE message_id = {}".format(self.message_id)).fetchone()[0]
        quest1 = cursor.execute("SELECT quest1 FROM requests WHERE message_id = {}".format(self.message_id)).fetchone()[0]
        quest2 = cursor.execute("SELECT quest2 FROM requests WHERE message_id = {}".format(self.message_id)).fetchone()[0]
        quest3 = cursor.execute("SELECT quest3 FROM requests WHERE message_id = {}".format(self.message_id)).fetchone()[0]
        quest4 = cursor.execute("SELECT quest4 FROM requests WHERE message_id = {}".format(self.message_id)).fetchone()[0]
        member = interaction.guild.get_member(id)
        embed = discord.Embed(title="Ваша заявка на вступление в город была отклонена!", description="Возможные причины отклонения *вашей* заявки: \n > 1. Имеются конфликты с администрацией\n\n > 2. Неправильно заполненная форма\n\n > 3. Вы были занесены в черный список города\n\n*Если ни один пункт для вас не окажется верным, обратитесь к меру города!*", color=embed_color)
        await member.send(embed=embed)
        cursor.execute("UPDATE requests SET clicked = 1 WHERE message_id = {}".format(interaction.message.id))
        cursor.execute("UPDATE requests SET otvet = 0 WHERE message_id = {}".format(interaction.message.id))
        connection.commit()
        embed = discord.Embed(
            description=f"**{quest1}** *написал анкету на вступление в город* (discord - {interaction.guild.get_member(id).mention})!\n\n> *Заявка была отклонена пользователем {interaction.user.mention}*",
            timestamp=datetime.utcnow(), color=embed_color)
        embed.add_field(name="Расскажите о себе:", value=f"{quest2}", inline=False)
        embed.add_field(name="Кем вы готовы стать в городе:", value=f"{quest3}", inline=False)
        embed.add_field(name="Чем вы готовы помочь городу:", value=f"{quest4}", inline=False)
        await interaction.message.edit(embed=embed)
        await interaction.response.send_message(f'Вы успешно отклонили заявку игрока {member.mention}!', ephemeral=True)

class Questionnaire(ui.Modal, title='Вступление в город'):
    name = ui.TextInput(label='Ваш никнейм')
    about = ui.TextInput(label='Расскажите о себе', style=discord.TextStyle.paragraph)
    kem = ui.TextInput(label='Кем вы готовы стать в городе?', style=discord.TextStyle.short)
    chem = ui.TextInput(label='Чем вы готовы помочь городу?')

    def __init__(self) -> None:
        super().__init__()



    async def on_submit(self, interaction: discord.Interaction):
        channel = interaction.guild.get_channel(1122573576483110962)
        embed = discord.Embed(description=f"**{self.name}** *написал анкету на вступление в город* (discord - {interaction.user.mention})!",
                              timestamp=datetime.utcnow(),
                              color=embed_color)
        embed.add_field(name="Расскажите о себе:", value=f"{self.about}", inline=False)
        embed.add_field(name="Кем вы готовы стать в городе:", value=f"{self.kem}", inline=False)
        embed.add_field(name="Расскажите о себе:", value=f"{self.chem}", inline=False)
        ff = await channel.send(embed=embed, view=Request_Method())
        await interaction.response.send_message('Ваша заявка успешно отправлена!', ephemeral=True)
        cursor.execute(f"INSERT INTO requests VALUES ({interaction.user.id}, {ff.id}, 0, \"{self.name}\", \"{self.about}\", \"{self.kem}\", \"{self.chem}\", NULL)")
        connection.commit()



class Request(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji='➕', custom_id='persistent_view:request_create')
    async def kz(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Questionnaire())



class invite_city(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        bot.add_view(Request_Method())
        bot.add_view(Request())

    @commands.has_any_role(1122550135340150806)
    @commands.command()
    async def gg(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Заявка на гражданина в город",
                              description="Чтобы подать заявку, нажмите на кнопку ниже, а затем заполните все нужные поля.",
                              color=embed_color)
        await interaction.channel.send(embed=embed, view=Request())

    @commands.Cog.listener()
    async def on_ready(self):
        global connection, cursor
        connection = sqlite3.connect("Leningrad.db")
        cursor = connection.cursor()
        print("[!] Base is loaded")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(invite_city(bot), guild=discord.Object(id=1038811883530108938))