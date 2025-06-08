import discord
from discord.ext import commands
import logging
from zoneinfo import zoneinfo

# ロギング 設定
_detail_formatting = "%(asctime)s - %(name)s - %(levelname)s - %(processName)-10s - %(threadName)s -\n*** %(message)s"

logging.basicConfig(
    level = logging.DEBUG,
    format = _detail_formatting, 
    filename = "./sample.log",
    encoding="utf-8"
)
console = logging.StreamHandler()
console_formatter = logging.Formatter("%(asctime)s : %(name)s : %(levelname)s : %(message)s")
console.setFormatter(console_formatter)
console.setLevel(logging.INFO) #consoleにはINFO
logging.getLogger("discord").addHandler(console)
logging.getLogger(__name__).addHandler(console)


log = logging.getLogger(__name__)

# Bot 設定
CHANNEL_ID = CHANNEL

# Bot のインスタンスを作成
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    log.info(f'Logged in as {bot.user} (ID: {bot.user.id})')
    # Bot 起動時に特定のチャンネルにメッセージを送信

# シャットダウン用コマンド
@bot.command()
async def shutdown(ctx):
    if ctx.author.guild_permissions.administrator:  # 管理者のみ実行可能
        await ctx.send("Shutting down bot...")
        await bot.close()  # Bot を停止
        log.info(f"Bot has been shutdown by {ctx.author.name}")
    else:
        await ctx.send("You don't have permission to shut down the bot.")

@bot.event
async def on_message(message):
    # メッセージがスレッド内に投稿されたか確認
    if message.channel.type == discord.ChannelType.public_thread:
        embed = discord.Embed( # Embedを定義する
                              color=0x00ff00, # フレーム色指定(今回は緑)
                              description=message.content
                              )
        embed.set_author(name=f"{message.author.name} @ {message.channel.name}", 
                         url=message.jump_url, 
                         icon_url=message.author.avatar.url 
                         )
        if message.attachments:
            if message.attachments[0].content_type.startswith("image"):
                embed.set_image(url=message.attachments[0].url)
        jst = ZoneInfo("Asia/Tokyo")
        local_dt = message.created_at.replace(tzinfo=ZoneInfo("UTC")).astimezone(jst)
        embed.set_footer(text=local_dt.strftime("%Y/%m/%d %H:%M:%S"))

        channel = bot.get_channel(CHANNEL_ID)

        await channel.send(embed=embed)

    await bot.process_commands(message)

# Bot トークン
bot.run("TOKEN")