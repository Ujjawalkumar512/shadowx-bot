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
whitelist_users = {OWNER_ID}
np_users = {OWNER_ID}   # owner default NP
warnings = {}
BAD_WORDS = ["mc", "bc", "gali, madarchod, bhosriwala, mkc, bkl, tmkc"]
settings = {
    "antinuke": False,
    "automod": True
}

# =========================
# BOT ONLINE
# =========================
@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.dnd,
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="🛡 ShadowX Security"
        )
    )
    print(f"{bot.user} is ready")


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
                f"{message.author.mention} bad words not allowed 🚫"
            )
            return

    # anti link
    if "http://" in msg or "https://" in msg:
        await message.delete()
        await message.channel.send(
            f"{message.author.mention} links not allowed 🔗🚫"
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
    await ctx.send(f"🏓 Pong! {round(bot.latency * 1000)}ms")

class HelpDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="General", emoji="🛠"),
            discord.SelectOption(label="Moderation", emoji="🛡"),
            discord.SelectOption(label="NP System", emoji="⚡")
        ]

        super().__init__(
            placeholder="Select module...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0]

        embed = discord.Embed(color=0x5865F2)

        if selected == "General":
            embed.title = "🛠 General Commands"
            embed.description = (
                ".ping\n"
                ".hello\n"
                ".avatar\n"
                ".profile"
            )

        elif selected == "Moderation":
            embed.title = "🛡 Moderation Commands"
            embed.description = (
                ".kick\n"
                ".ban\n"
                ".unban\n"
                ".clear\n"
                ".warn\n"
                ".unwarn"
            )

        elif selected == "NP System":
            embed.title = "⚡ NP System"
            embed.description = (
                ".npadd\n"
                ".npremove\n"
                ".nplist"
            )

        await interaction.response.edit_message(embed=embed, view=self.view)

class HelpMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(HelpDropdown())

@bot.command(name="help")
async def help_menu(ctx):
    embed = discord.Embed(
        title="⚡ ShadowX Help Panel",
        description="Select category below 👇",
        color=0x5865F2
    )

    await ctx.send(embed=embed, view=HelpMenu())

# =========================
# NP SYSTEM
# =========================
@bot.command()
async def npadd(ctx, user_id: int):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Sirf owner use kar sakta hai")
        return

    np_users.add(user_id)
    await ctx.send(f" ✔ NP add ho gaya: {user_id}")

@bot.command()
async def npremove(ctx, user_id: int):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Sirf owner use kar sakta hai")
        return

    np_users.discard(user_id)
    await ctx.send(f" ✔ NP remove ho gaya: {user_id}")

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
        f"{amount} Deleted messages.",
        delete_after=3
    )

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason"):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} has been kiked.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason"):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} has been baned.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user)

    await ctx.send(f"🔓 Unbanned {user.name}")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(
        ctx.guild.default_role,
        send_messages=False
    )
    await ctx.send(f" ✔ <#{ctx.channel.id}> has been locked.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(
        ctx.guild.default_role,
        send_messages=True
    )
    await ctx.send(f" ✔ <#{ctx.channel.id}> has been unlocked.")

# =========================
# WARN SYSTEM
# =========================
@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason="No reason"):
    if member.id not in warnings:
        warnings[member.id] = []

    warnings[member.id].append(reason)

    count = len(warnings[member.id])

    await ctx.send(
        f"{member.mention} has been warned.\n"
        f"Reason: {reason}\n"
        f"Total warns: {count}"
    )

@bot.command()
@commands.has_permissions(manage_messages=True)
async def unwarn(ctx, member: discord.Member):
    if member.id not in warnings or not warnings[member.id]:
        return await ctx.send("❌ No warnings found")

    removed = warnings[member.id].pop()

    await ctx.send(
        f"🔓 Removed warning from {member.mention}\n"
        f"Removed: {removed}"
    )

@bot.command()
async def warns(ctx, member: discord.Member):
    if member.id not in warnings or not warnings[member.id]:
        return await ctx.send("✅ No warnings")

    warn_list = "\n".join(
        [f"{i+1}. {w}" for i, w in enumerate(warnings[member.id])]
    )

    await ctx.send(
        f"⚠️ Warnings for {member.mention}:\n{warn_list}"
    )


@bot.command()
async def status(ctx):
    await ctx.send(
        f"✔ AntiNuke: {'ON' if settings['antinuke'] else 'OFF'}\n"
        f"✔ AutoMod: {'ON' if settings['automod'] else 'OFF'}"
    )

# ================= ANTI NUKE =================
@bot.command()
@commands.has_permissions(administrator=True)
async def antinuke(ctx, mode: str):
    if mode.lower() == "enable":
        settings["antinuke"] = True
        await ctx.send("✔ AntiNuke ENABLED")

    elif mode.lower() == "disable":
        settings["antinuke"] = False
        await ctx.send("❌ AntiNuke DISABLED")

    else:
        await ctx.send("Usage: .antinuke enable/disable")

# ================= AUTOMOD =================
@bot.command()
@commands.has_permissions(administrator=True)
async def automod(ctx, mode: str):
    if mode.lower() == "enable":
        settings["automod"] = True
        await ctx.send("✔ AutoMod ENABLED")

    elif mode.lower() == "disable":
        settings["automod"] = False
        await ctx.send("❌ AutoMod DISABLED")

    else:
        await ctx.send("Usage: .automod enable/disable")

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author

    embed = discord.Embed(
        title=f"🖼 Avatar of {member}",
        color=0x5865F2
    )

    embed.set_image(url=member.display_avatar.url)
    embed.set_footer(text="ShadowX Avatar System")

    await ctx.send(embed=embed)

@bot.command()
async def profile(ctx, member: discord.Member = None):
    member = member or ctx.author

    embed = discord.Embed(
        title=f"👤 Profile of {member}",
        color=0x2ecc71
    )

    embed.set_thumbnail(url=member.display_avatar.url)

    embed.add_field(name="Name", value=member.name, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d"), inline=False)

    embed.set_footer(text="ShadowX Profile System")

    await ctx.send(embed=embed)

@bot.command()
async def servericon(ctx):
    embed = discord.Embed(
        title="🖼 Server Icon",
        color=0xe74c3c
    )

    embed.set_image(url=ctx.guild.icon.url if ctx.guild.icon else None)

    await ctx.send(embed=embed)

@bot.command()
async def serverbanner(ctx):
    if ctx.guild.banner:
        embed = discord.Embed(
            title="🎨 Server Banner",
            color=0xf1c40f
        )
        embed.set_image(url=ctx.guild.banner.url)
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ Server banner not available")

def is_whitelisted():
    async def predicate(ctx):
        return ctx.author.id in whitelist_users
    return commands.check(predicate)

@bot.command()
async def wladd(ctx, user_id: int):
    if ctx.author.id != OWNER_ID:
        return await ctx.send("❌ Only owner can use this")

    whitelist_users.add(user_id)
    await ctx.send(f"✅ Added {user_id} to whitelist")

@bot.command()
async def wlremove(ctx, user_id: int):
    if ctx.author.id != OWNER_ID:
        return await ctx.send("❌ Only owner can use this")

    if user_id == OWNER_ID:
        return await ctx.send("❌ Owner cannot be removed")

    whitelist_users.discard(user_id)
    await ctx.send(f"🗑 Removed {user_id} from whitelist")

@bot.command()
async def whitelist(ctx):
    if ctx.author.id != OWNER_ID:
        return await ctx.send("❌ Only owner can use this")

    users = "\n".join(str(uid) for uid in whitelist_users)
    await ctx.send(f"🛡 Whitelisted Users:\n{users}")



import os
bot.run(os.getenv("TOKEN"))
