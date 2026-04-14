import discord
from discord.ext import commands

# =========================
# BOT SETUP
# =========================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix=".",
    intents=intents,
    help_command=None
)

# =========================
# CONFIG
# =========================
OWNER_ID = 1458873558502478095
np_users = {OWNER_ID}   # owner default NP
warnings = {}
BAD_WORDS = ["mc", "bc", "gali"]

# =========================
# BOT ONLINE
# =========================
@bot.event
async def on_ready():
    print("ShadowX online ho gaya 🔥")

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="your server ⚡"
        )
    )

# =========================
# JOIN + AUTOROLE
# =========================
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="Member")

    if role:
        await member.add_roles(role)

    channel = member.guild.system_channel
    if channel:
        await channel.send(
            f"Welcome {member.mention} 🔥 ShadowX me swagat hai!"
        )

# =========================
# LEAVE LOG
# =========================
@bot.event
async def on_member_remove(member):
    channel = member.guild.system_channel
    if channel:
        await channel.send(
            f"{member.name} server leave kar gaya 😢"
        )

# =========================
# AUTO MOD + NP SYSTEM
# =========================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    msg = message.content.lower()

    # bad words filter
    for word in BAD_WORDS:
        if word in msg:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention} bad words allowed nahi hai 🚫"
            )
            return

    # anti link
    if "http://" in msg or "https://" in msg:
        await message.delete()
        await message.channel.send(
            f"{message.author.mention} links allowed nahi hai 🔗🚫"
        )
        return

    # no prefix for selected users
    if message.author.id in np_users and not message.content.startswith("."):
        message.content = "." + message.content

    await bot.process_commands(message)

# =========================
# BASIC COMMANDS
# =========================
@bot.command()
async def hello(ctx):
    await ctx.send("Hello bhai 🔥")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong 🏓")

# =========================
# HELP MENU
# =========================
@bot.command(name="help")
async def help_menu(ctx):
    embed = discord.Embed(
        title="⚡ ShadowX Help Menu ⚡",
        description="Powerful multipurpose Discord bot",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="🛠 General",
        value="ping\nhello\nhelp",
        inline=False
    )

    embed.add_field(
        name="🛡 Moderation",
        value="kick\nban\nclear\nlock\nunlock\nwarn",
        inline=False
    )

    embed.add_field(
        name="⚡ NP System",
        value="npadd <id>\nnpremove <id>\nnplist",
        inline=False
    )

    embed.set_footer(text="ShadowX Powered by 1tz.jack 🔥")
    await ctx.send(embed=embed)

# =========================
# NP SYSTEM
# =========================
@bot.command()
async def npadd(ctx, user_id: int):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Sirf owner use kar sakta hai")
        return

    np_users.add(user_id)
    await ctx.send(f"✅ NP add ho gaya: {user_id}")

@bot.command()
async def npremove(ctx, user_id: int):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Sirf owner use kar sakta hai")
        return

    np_users.discard(user_id)
    await ctx.send(f"✅ NP remove ho gaya: {user_id}")

@bot.command()
async def nplist(ctx):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Sirf owner use kar sakta hai")
        return

    await ctx.send(f"⚡ NP Users: {list(np_users)}")

# =========================
# MODERATION
# =========================
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(
        f"{amount} messages delete kar diye 🧹",
        delete_after=3
    )

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason"):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} ko kick kar diya 👢")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason"):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} ko ban kar diya 🔨")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(
        ctx.guild.default_role,
        send_messages=False
    )
    await ctx.send("Channel lock kar diya 🔒")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(
        ctx.guild.default_role,
        send_messages=True
    )
    await ctx.send("Channel unlock kar diya 🔓")

# =========================
# WARN SYSTEM
# =========================
@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason="No reason"):
    if member.id not in warnings:
        warnings[member.id] = 0

    warnings[member.id] += 1
    count = warnings[member.id]

    await ctx.send(
        f"{member.mention} ko warn diya ⚠️\n"
        f"Reason: {reason}\n"
        f"Total warns: {count}"
    )

    if count >= 3:
        muted_role = discord.utils.get(
            ctx.guild.roles,
            name="Muted"
        )

        if muted_role is None:
            muted_role = await ctx.guild.create_role(
                name="Muted"
            )

            for channel in ctx.guild.channels:
                await channel.set_permissions(
                    muted_role,
                    send_messages=False
                )

        await member.add_roles(muted_role)

        await ctx.send(
            f"{member.mention} ko 3 warns ke baad mute kar diya 🔇"
        )



import os
bot.run(os.getenv("TOKEN"))
