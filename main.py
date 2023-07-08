from datetime import datetime
import asyncio
import discord
import discord.ext.commands as commands
import sqlite3
import asyncio
import psutil
from discord import ui
from discord.utils import get

global cursor, connection
token = ''
global embed_color
embed_color = 0x36393f


class PersistentViewBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix='!', intents=discord.Intents.all())

    async def setup_hook(self):
        await bot.tree.sync(guild=discord.Object(id=1038811883530108938))
        await bot.load_extension('cogs.country_choose')
        await bot.load_extension('cogs.invite_city')

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("У вас нет прав на выполнение данной команды.")
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("Команда не найдена!")

    async def on_ready(self):
        CPU = psutil.cpu_percent()
        mem = psutil.virtual_memory()
        percentmem = int(mem.percent)
        print(
            f"\n_-_-_-_-_-_-_-_-_-_-_-_-\n\nLeningrad bot\n𝕯𝖊𝖛𝖊𝖑𝖔𝖕 𝕸𝖆𝖞𝖔𝖗𝕷𝖊𝖔𝖓\n\n-_-_-_-_-_-_-_-_-_-_-_-_\nИнформация о боте:\nЗагруженность процессора: {CPU}%\nЗагруженность памяти: {percentmem}%")
        print(f"--------\nТокен: {token}")
        connection = sqlite3.connect("Leningrad.db")
        cursor = connection.cursor()
        if connection:
            print("--------\nБаза подключена\n--------")
            cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        				name TEXT,
        				id INT
        		)""")
            cursor.execute("""CREATE TABLE IF NOT EXISTS requests (
                    				id INT, 
                    				message_id INT,
                    				clicked INT,
                    				quest1 TEXT,
                    				quest2 TEXT,
                    				quest3 TEXT,
                    				quest4 TEXT,
                    				otvet INT
                    		)""")
            print("проверка бип бип")
            connection.commit()
        for guild in self.guilds:
            for member in guild.members:
                if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                    cursor.execute(f"INSERT INTO users VALUES (\"{member}\", \"{member.id}\")")
                    connection.commit()
                else:
                    pass
        connection.commit()
        info = "!"
        print("[{}] Бот готов к работе.".format(info))  # в командную строку идёт инфа о запуске
        while True:
            await self.change_presence(status=discord.Status.idle, activity=discord.Activity(name=f'за чебоксарами',
                                                                                             type=discord.ActivityType.watching))  # Идёт инфа о команде помощи (префикс изменить)
            await asyncio.sleep(15)


bot = PersistentViewBot()

bot.run(token)
