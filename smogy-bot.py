from logging import error
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, has_role
import discord
import asyncio
from discord_slash import SlashCommand, SlashContext, error
#import youtube_dl


load_dotenv(dotenv_path="config")

bot = commands.Bot(command_prefix="/")
bot.remove_command("help")
slash = SlashCommand(bot, sync_commands=True)


image_error="https://i.ibb.co/tHWL83V/acces-denied.png"
image_acces="https://i.ibb.co/nPwnQmL/9up7-T4j-Imgur.png"

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('twitch.tv/smogyyyy'))
    print("Bot prêt !")


@slash.slash(name="Clear", description="Effacer des messages")
@has_permissions(manage_messages=True)
async def clear(ctx, nombre: int):
    author = ctx.author
    channel = ctx.channel
    channel_logs = bot.get_channel(848578058906238996)
    messages = await ctx.channel.history(limit=nombre + 1).flatten()
    for message in messages:
        await message.delete()
    embed = discord.Embed(title=f"Le channel "f"#{channel}" " a été clear !", color=0xe6de00)
    embed.set_thumbnail(url=image_acces)
    embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
    await channel_logs.send(embed=embed)

@error.SlashCommandError
async def clear_error(ctx, error):
    if isinstance(error, MissingPermissions):
        author = ctx.author
        embed = discord.Embed(title="Permissions insufisantes",
                              description=f"{author.mention} Vous devez avoir la permission : **manage_messages**", color=0xf09400)
        embed.set_thumbnail(url=image_error)
        await author.send(embed=embed)


@slash.slash(name="Ban", description="Bannir un membre définitivement")
@has_permissions(ban_members=True)
async def ban(ctx, user: discord.User, *, reason="Aucune raison donnée"):
    channel_logs = bot.get_channel(848578058906238996)
    author = ctx.author
    embed = discord.Embed(title=f"{user.name} a été **ban** !",
                          description="Cet utilisateur n'a pas respecté les règles du serveur !", color=0xcc0202)
    embed.set_thumbnail(url=image_acces)
    embed.add_field(name="Utilisateur banni", value=user.mention, inline=True)
    embed.add_field(name="Raison", value=reason, inline=True)
    embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
    await channel_logs.send(embed=embed)
    embed_user = discord.Embed(title="Vous avez été banni !",
                               description="Il semblerait que vous n'ayez pas respecté les règles du serveur. "
                                           "Si la raison de votre bannissement vous semble incorrecte, "
                                           "vous pouvez contacter le modérateur qui vous a banni !", color=0xcc0202)
    embed_user.set_thumbnail(url= image_acces)
    embed_user.add_field(name="Raison", value=reason, inline=True)
    embed_user.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
    await user.send(embed=embed_user)
    await ctx.guild.ban(user, reason=reason)


@error.SlashCommandError
async def ban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        author = ctx.author
        embed = discord.Embed(title="Permissions insufisantes",
                              description=f"{author.mention} Vous devez avoir la permission : **ban_members**", color=0xf09400)
        embed.set_thumbnail(url=image_error)
        await author.send(embed=embed)


@bot.command()
@has_permissions(kick_members=True)
async def kick(ctx, user: discord.User, *, reason="Aucune raison donnée"):
    channel_logs = bot.get_channel(848578058906238996)
    author = ctx.author
    embed = discord.Embed(title=f"{user.name} a été **kick** !",
                          description=f"Cet utilisateur n'a pas respecté les règles du serveur !", color=0xcc0202)
    embed.set_thumbnail(url=image_acces)
    embed.add_field(name="Utilisateur kick", value=user.mention, inline=True)
    embed.add_field(name="Raison", value=reason, inline=True)
    embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
    embed.set_footer()
    await channel_logs.send(embed=embed)
    embed_user = discord.Embed(title="Vous avez été kick !",
                               description="Il semblerait que vous n'ayez pas respecté les règles du serveur. "
                                           "Si la raison de votre kick vous semble incorrecte, "
                                           "vous pouvez contacter le modérateur qui vous a kick"
                                           "vous pouvez revenir sur le serveur via le lien ci-dessous.", color=0xcc0202)
    embed_user.set_thumbnail(url=image_acces)
    embed_user.add_field(name="Raison", value=reason, inline=True)
    embed_user.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
    embed_user.add_field(name="Discord", value="https://discord.gg/fqEpWkQdcf", inline=True)
    await user.send(embed=embed_user)
    await ctx.guild.kick(user, reason=reason)



@kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingPermissions):
        author = ctx.author
        embed = discord.Embed(title="Permissions insufisantes",
                              description=f"{author.mention} Vous devez avoir la permission : **kick_members**", color=0xf09400)
        embed.set_thumbnail(url=image_error)
        await author.send(embed=embed)


@bot.command()
@has_permissions(ban_members=True)
async def unban(ctx, user, *, reason="Aucune raison donnée"):
	reason = " ".join(reason)
	userName, userId = user.split("#")
	bannedUsers = await ctx.guild.bans()
	for i in bannedUsers:
		if i.user.name == userName and i.user.discriminator == userId:
			await ctx.guild.unban(i.user, reason = reason)
			await author.send(f"{user} à été unban.")
			return
	#Ici on sait que lutilisateur na pas ete trouvé
	await author.send(f"L'utilisateur {user} n'est pas dans la liste des bans")


@unban.error
async def unban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        author = ctx.author
        embed = discord.Embed(title="Permissions insufisantes",
                              description=f"{author.mention} Vous devez avoir la permission : **ban_members**",
                              color=0xf09400)
        embed.set_thumbnail(url=image_error)
        await author.send(embed=embed)



@bot.command()
@has_permissions(ban_members=True)
async def tempban(ctx, user: discord.User, duration: int, time, *, reason="Aucune raison donnée"):
    channel_logs = bot.get_channel(848578058906238996)
    author = ctx.author
    if "s" == time:
        embed = discord.Embed(title=f"{user.name} a été **ban temporairement** !",
                              description=f"Cet utilisateur n'a pas respecté les règles du serveur !", color=0xcc0202)
        embed.add_field(name="Utilisateur banni", value=user.mention, inline=True)
        embed.add_field(name="Raison", value=reason, inline=True)
        embed.add_field(name="Durée", value=f"{duration} seconde(s)", inline=True)
        embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        embed.set_thumbnail(url=image_acces)
        await channel_logs.send(embed=embed)
        embed_user = discord.Embed(title="Vous avez été banni temporairement !",
                                   description="Il semblerait que vous n'ayez pas respecté les règles du serveur. "
                                               "Si la raison de votre ban vous semble incorrecte, "
                                               "vous pouvez contacter le modérateur qui vous a banni."
                                               "**Vous pourrez revenir sur le serveur via le lien ci-dessous une fois que votre ban "
                                               "sera terminé.**",
                                   color=0xcc0202)
        embed_user.add_field(name="Raison", value=reason, inline=True)
        embed_user.add_field(name="Temps de banissement", value=f"{duration} seconde(s)", inline=True)
        embed_user.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        embed_user.add_field(name="Discord", value="https://discord.gg/fqEpWkQdcf", inline=True)
        embed_user.set_thumbnail(url=image_error)
        await user.send(embed=embed_user)
        await ctx.guild.ban(user, reason=reason)
        await asyncio.sleep(duration)
        await ctx.guild.unban(user)
    elif "m" == time:
        duration_min = duration * 60
        embed = discord.Embed(title=f"{user.name} a été **ban temporairement** !",
                              description=f"Cet utilisateur n'a pas respecté les règles du serveur !", color=0xcc0202)
        embed.set_thumbnail(url=image_acces)
        embed.add_field(name="Utilisateur banni", value=user.mention, inline=True)
        embed.add_field(name="Raison", value=reason, inline=True)
        embed.add_field(name="Durée", value=f"{duration} minute(s)", inline=True)
        embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        await channel_logs.send(embed=embed)
        embed_user = discord.Embed(title="Vous avez été banni temporairement !",
                                   description="Il semblerait que vous n'ayez pas respecté les règles du serveur. "
                                               "Si la raison de votre ban vous semble incorrecte, "
                                               "vous pouvez contacter le modérateur qui vous a banni."
                                               "**Vous pourrez revenir sur le serveur via le lien ci-dessous une fois que votre ban "
                                               "sera terminé.**",
                                   color=0xcc0202)
        embed_user.set_thumbnail(url=image_error)
        embed_user.add_field(name="Raison", value=reason, inline=True)
        embed_user.add_field(name="Temps de banissement", value=f"{duration} minute(s)", inline=True)
        embed_user.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        embed_user.add_field(name="Discord", value="https://discord.gg/fqEpWkQdcf", inline=True)
        await user.send(embed=embed_user)
        await ctx.guild.ban(user, reason=reason)
        await asyncio.sleep(duration_min)
        await ctx.guild.unban(user)
    elif "h" == time:
        duration_heure = duration * 3600
        embed = discord.Embed(title=f"{user.name} a été **ban temporairement** !",
                              description=f"Cet utilisateur n'a pas respecté les règles du serveur !", color=0xcc0202)
        embed.set_thumbnail(url=image_acces)
        embed.add_field(name="Utilisateur banni", value=user.mention, inline=True)
        embed.add_field(name="Raison", value=reason, inline=True)
        embed.add_field(name="Durée", value=f"{duration} heure(s)", inline=True)
        embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        await channel_logs.send(embed=embed)
        embed_user = discord.Embed(title="Vous avez été banni temporairement !",
                                   description="Il semblerait que vous n'ayez pas respecté les règles du serveur. "
                                               "Si la raison de votre ban vous semble incorrecte, "
                                               "vous pouvez contacter le modérateur qui vous a banni."
                                               "**Vous pourrez revenir sur le serveur via le lien ci-dessous une fois que votre ban "
                                               "sera terminé.**",
                                   color=0xcc0202)
        embed_user.set_thumbnail(url=image_error)
        embed_user.add_field(name="Raison", value=reason, inline=True)
        embed_user.add_field(name="Temps de banissement", value=f"{duration} heure(s)", inline=True)
        embed_user.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        embed_user.add_field(name="Discord", value="https://discord.gg/fqEpWkQdcf", inline=True)
        await user.send(embed=embed_user)
        await ctx.guild.ban(user, reason=reason)
        await asyncio.sleep(duration_heure)
        await ctx.guild.unban(user)
    elif "j" == time:
        duration_jour = duration * 86400
        embed = discord.Embed(title=f"{user.name} a été **ban temporairement** !",
                              description=f"Cet utilisateur n'a pas respecté les règles du serveur !", color=0xcc0202)
        embed.set_thumbnail(url=image_acces)
        embed.add_field(name="Utilisateur banni", value=user.mention, inline=True)
        embed.add_field(name="Raison", value=reason, inline=True)
        embed.add_field(name="Durée", value=f"{duration} jour(s)", inline=True)
        embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        await channel_logs.send(embed=embed)
        embed_user = discord.Embed(title="Vous avez été banni temporairement !",
                                   description="Il semblerait que vous n'ayez pas respecté les règles du serveur. "
                                               "Si la raison de votre ban vous semble incorrecte, "
                                               "vous pouvez contacter le modérateur qui vous a banni."
                                               "**Vous pourrez revenir sur le serveur via le lien ci-dessous une fois que votre ban "
                                               "sera terminé.**",
                                   color=0xcc0202)
        embed_user.set_thumbnail(url=image_error)
        embed_user.add_field(name="Raison", value=reason, inline=True)
        embed_user.add_field(name="Temps de banissement", value=f"{duration} jour(s)", inline=True)
        embed_user.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        embed_user.add_field(name="Discord", value="https://discord.gg/fqEpWkQdcf", inline=True)
        await user.send(embed=embed_user)
        await ctx.guild.ban(user, reason=reason)
        await asyncio.sleep(duration_jour)
        await ctx.guild.unban(user)
    elif "mois" == duration:
        duration_mois = duration * 86400 * 30
        embed = discord.Embed(title=f"{user.name} a été **ban temporairement** !",
                              description=f"Cet utilisateur n'a pas respecté les règles du serveur !", color=0xcc0202)
        embed.set_thumbnail(url=image_acces)
        embed.add_field(name="Utilisateur banni", value=user.mention, inline=True)
        embed.add_field(name="Raison", value=reason, inline=True)
        embed.add_field(name="Durée", value=f"{duration} mois", inline=True)
        embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        await channel_logs.send(embed=embed)
        embed_user = discord.Embed(title="Vous avez été banni temporairement !",
                                   description="Il semblerait que vous n'ayez pas respecté les règles du serveur. "
                                               "Si la raison de votre ban vous semble incorrecte, "
                                               "vous pouvez contacter le modérateur qui vous a banni. "
                                               "**Vous pourrez revenir sur le serveur via le lien ci-dessous une fois que votre ban "
                                               "sera terminé.**",
                                   color=0xcc0202)
        embed_user.set_thumbnail(url=image_error)
        embed_user.add_field(name="Raison", value=reason, inline=True)
        embed_user.add_field(name="Temps de banissement", value=f"{duration} mois", inline=True)
        embed_user.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        embed_user.add_field(name="Discord", value="https://discord.gg/fqEpWkQdcf", inline=True)
        await user.send(embed=embed_user)
        await ctx.guild.ban(user, reason=reason)
        await asyncio.sleep(duration_mois)
        await ctx.guild.unban(user)
    else:
        author = ctx.author
        embed = discord.Embed(title="Valeur de l'argument **[temps]** est inconnue",
                              description=f"{author.mention} L'argument [temps] doit être : **[s, m, j, mois]**", color=0xf09400)
        embed.set_thumbnail(url=image_error)
        embed.add_field(name="s", value="seconde(s)", inline=True)
        embed.add_field(name="h", value="heure(s)", inline=True)
        embed.add_field(name="j", value="jour(s)", inline=True)
        embed.add_field(name="mois", value="mois", inline=True)
        await ctx.send(embed=embed)


@tempban.error
async def tempban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        author = ctx.author
        embed = discord.Embed(title="Permissions insufisantes",
                              description=f"{author.mention} Vous devez avoir la permission : **ban_members**", color=0xf09400)
        embed.set_thumbnail(url=image_error)
        await author.send(embed=embed)

async def createRoleMute(ctx):
    role_mute = await ctx.guild.create_role(name = "mute",
                                            permissions= discord.Permissions(send_messages= False, speak= False))
    for channel in ctx.guild.channels:
        await channel.set_permissions(role_mute, send_messages=False, speak= False)


async def getRoleMute(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "mute":
            return role

    return await createRoleMute(ctx)

@bot.command()
@has_permissions(manage_roles=True)
async def tempmute(ctx, user: discord.User, duration: int, time, *, reason="Aucune raison donnée"):
    channel_logs = bot.get_channel(848578058906238996)
    role_mute = await getRoleMute(ctx)
    author = ctx.author
    if "s" == time:
        embed = discord.Embed(title=f"{user.name} a été **mute temporairement** !",
                              description=f"Cet utilisateur n'a pas respecté les règles du serveur !", color=0xcc0202)
        embed.add_field(name="Utilisateur mute", value=user.mention, inline=True)
        embed.add_field(name="Raison", value=reason, inline=True)
        embed.add_field(name="Durée", value=f"{duration} seconde(s)", inline=True)
        embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        embed.set_thumbnail(url=image_acces)
        await channel_logs.send(embed=embed)
        embed_user = discord.Embed(title="Vous avez été mute !",
                                   description="Il semblerait que vous n'ayez pas respecté les règles du serveur. "
                                               "Si la raison de votre mute vous semble incorrecte, "
                                               "vous vous contacter le modérateur qui vous a mute.",
                                   color=0xcc0202)
        embed_user.add_field(name="Raison", value=reason, inline=True)
        embed_user.add_field(name="Temps de mute", value=f"{duration} seconde(s)", inline=True)
        embed_user.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        embed_user.set_thumbnail(url=image_error)
        await user.send(embed=embed_user)
        await user.add_roles(role_mute, reason=reason)
        await asyncio.sleep(duration)
        await user.remove_roles(role_mute, reason="Fin de la période de mute")
    elif "m" == time:
        duration_min = duration * 60
        embed = discord.Embed(title=f"{user.name} a été **ban temporairement** !",
                              description=f"Cet utilisateur n'a pas respecté les règles du serveur !", color=0xcc0202)
        embed.set_thumbnail(url=image_acces)
        embed.add_field(name="Utilisateur mute", value=user.mention, inline=True)
        embed.add_field(name="Raison", value=reason, inline=True)
        embed.add_field(name="Durée", value=f"{duration} minute(s)", inline=True)
        embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        await channel_logs.send(embed=embed)
        embed_user = discord.Embed(title="Vous avez été mute !",
                                   description="Il semblerait que vous n'ayez pas respecté les règles du serveur. "
                                               "Si la raison de votre mute vous semble incorrecte, "
                                               "vous vous contacter le modérateur qui vous a mute.",
                                   color=0xcc0202)
        embed_user.set_thumbnail(url=image_error)
        embed_user.add_field(name="Raison", value=reason, inline=True)
        embed_user.add_field(name="Temps de mute", value=f"{duration} minute(s)", inline=True)
        embed_user.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        await user.send(embed=embed_user)
        await user.add_roles(role_mute, reason=reason)
        await asyncio.sleep(duration_min)
        await user.remove_roles(role_mute, reason="Fin de la période de mute")
    elif "h" == time:
        duration_heure = duration * 3600
        embed = discord.Embed(title=f"{user.name} a été **mute temporairement** !",
                              description=f"Cet utilisateur n'a pas respecté les règles du serveur !", color=0xcc0202)
        embed.set_thumbnail(url=image_acces)
        embed.add_field(name="Utilisateur mute", value=user.mention, inline=True)
        embed.add_field(name="Raison", value=reason, inline=True)
        embed.add_field(name="Durée", value=f"{duration} heure(s)", inline=True)
        embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        await channel_logs.send(embed=embed)
        embed_user = discord.Embed(title="Vous avez été mute !",
                                   description="Il semblerait que vous n'ayez pas respecté les règles du serveur. "
                                               "Si la raison de votre mute vous semble incorrecte, "
                                               "vous vous contacter le modérateur qui vous a mute.",
                                   color=0xcc0202)
        embed_user.set_thumbnail(url=image_error)
        embed_user.add_field(name="Raison", value=reason, inline=True)
        embed_user.add_field(name="Temps de banissement", value=f"{duration} heure(s)", inline=True)
        embed_user.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        await user.send(embed=embed_user)
        await user.add_roles(role_mute, reason=reason)
        await asyncio.sleep(duration_heure)
        await user.remove_roles(role_mute, reason="Fin de la période de mute")
    elif "j" == time:
        duration_jour = duration * 86400
        embed = discord.Embed(title=f"{user.name} a été **mute temporairement** !",
                              description=f"Cet utilisateur n'a pas respecté les règles du serveur !", color=0xcc0202)
        embed.set_thumbnail(url=image_acces)
        embed.add_field(name="Utilisateur mute", value=user.mention, inline=True)
        embed.add_field(name="Raison", value=reason, inline=True)
        embed.add_field(name="Durée", value=f"{duration} jour(s)", inline=True)
        embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        await channel_logs.send(embed=embed)
        embed_user = discord.Embed(title="Vous avez été mute !",
                                   description="Il semblerait que vous n'ayez pas respecté les règles du serveur. "
                                               "Si la raison de votre mute vous semble incorrecte, "
                                               "vous vous contacter le modérateur qui vous a mute.",
                                   color=0xcc0202)
        embed_user.set_thumbnail(url=image_error)
        embed_user.add_field(name="Raison", value=reason, inline=True)
        embed_user.add_field(name="Temps de mute", value=f"{duration} jour(s)", inline=True)
        embed_user.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        await user.send(embed=embed_user)
        await user.add_roles(role_mute, reason=reason)
        await asyncio.sleep(duration_jour)
        await user.remove_roles(role_mute, reason="Fin de la période de mute")
    elif "mois" == duration:
        duration_mois = duration * 86400 * 30
        embed = discord.Embed(title=f"{user.name} a été **mute temporairement** !",
                              description=f"Cet utilisateur n'a pas respecté les règles du serveur !", color=0xcc0202)
        embed.set_thumbnail(url=image_acces)
        embed.add_field(name="Utilisateur mute", value=user.mention, inline=True)
        embed.add_field(name="Raison", value=reason, inline=True)
        embed.add_field(name="Durée", value=f"{duration} mois", inline=True)
        embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        await channel_logs.send(embed=embed)
        embed_user = discord.Embed(title="Vous avez été mute !",
                                   description="Il semblerait que vous n'ayez pas respecté les règles du serveur. "
                                               "Si la raison de votre mute vous semble incorrecte, "
                                               "vous vous contacter le modérateur qui vous a mute.",
                                   color=0xcc0202)
        embed_user.set_thumbnail(url=image_error)
        embed_user.add_field(name="Raison", value=reason, inline=True)
        embed_user.add_field(name="Temps de mute", value=f"{duration} mois", inline=True)
        embed_user.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        await user.send(embed=embed_user)
        await user.add_roles(role_mute, reason=reason)
        await asyncio.sleep(duration_mois)
        await user.remove_roles(role_mute, reason="Fin de la période de mute")
    else:
        author = ctx.author
        embed = discord.Embed(title="Valeur de l'argument **[temps]** est inconnue",
                              description=f"{author.mention} L'argument [temps] doit être : **[s, m, j, mois]**",
                              color=0xf09400)
        embed.set_thumbnail(url=image_error)
        embed.add_field(name="s", value="seconde(s)", inline=True)
        embed.add_field(name="h", value="heure(s)", inline=True)
        embed.add_field(name="j", value="jour(s)", inline=True)
        embed.add_field(name="mois", value="mois", inline=True)
        await ctx.send(embed=embed)

@tempmute.error
async def tempmute_error(ctx, error):
    if isinstance(error, MissingPermissions):
        author = ctx.author
        embed = discord.Embed(title="Permissions insufisantes",
                              description=f"{author.mention} Vous devez avoir la permission : **manage_roles**", color=0xf09400)
        embed.set_thumbnail(url=image_error)
        await author.send(embed=embed)

@bot.command()
@has_permissions(manage_roles=True)
async def unmute(ctx, user: discord.User, *, reason="Aucune raison donnée"):
    channel_logs = bot.get_channel(848578058906238996)
    author = ctx.author
    role_mute = await getRoleMute(ctx)
    await user.add_roles(role_mute, reason=reason)
    await user.remove_roles(role_mute, reason="Fin de la période de mute")
    embed = discord.Embed(title=f"{user} été de-mute !",
                              description="Il peut maintenant re-parler dans le chat !",
                              color=0x42f557)
    embed.set_thumbnail(url=image_acces)
    embed.add_field(name="Raison", value=reason, inline=True)
    embed.add_field(name="Modérateur", value=f"{ctx.author.mention}", inline=True)
    await channel_logs.send(embed=embed)
    embed_user = discord.Embed(title="Vous avez été de-mute !",
                               description="Vous pouvez maintenant re-parler dans le chat !",
                               color=0x42f557)
    embed_user.set_thumbnail(url=image_acces)
    embed_user.add_field(name="Raison", value=reason, inline=True)
    embed_user.add_field(name="Modérateur", value=f"vous avez été démute par {ctx.author.mention}", inline=True)
    await user.send(embed=embed_user)


@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, MissingPermissions):
        author = ctx.author
        embed = discord.Embed(title="Permissions insufisantes",
                              description=f"{author.mention} Vous devez avoir la permission : **manage_roles**", color=0xf09400)
        embed.set_thumbnail(url=image_error)
        await author.send(embed=embed)

@bot.command()
async def help(ctx):
    author= ctx.author
    embed= discord.Embed(title="Liste des commandes", color=0x4287f5)
    embed.add_field(name="/ban [@user] [raison:optionnelle]", value="```Permet de bannir définitivement un membre```", inline=False)
    embed.add_field(name="/tempban [@user] [temps de ban (EN NOMBRE) exemple : 1 ; 13 ; 21] [unité du temps de ban exemple : s; h; j; mois] [raison:optionnelle]", value="```Permet de bannir temporairement un membre```", inline=False)
    embed.add_field(name="/unban [user#1234] [raison:optionnelle]", value="```Permet d'unban un membre banni```", inline=False)
    embed.add_field(name="/clear [nombre de message à supprimer]", value="```Permet de supprimer plusieurs messages```", inline=False)
    embed.add_field(name="/kick [@user] [raison:optionnelle]", value="```Permet d'exclure un membre```", inline=False)
    embed.add_field(name="/tempmute [@user] [temps de mute (EN NOMBRE) exemple : 1 ; 13 ; 21] [unité du temps de mute exemple : s; h; j; mois] [raison:optionnelle]", value="```Permet de bannir temporairement un membre```", inline=False)
    embed.add_field(name="/unmute [@user] [raison:optionnelle]", value="```Permet de demute un membre```", inline=False)
    embed.set_thumbnail(url="https://i.ibb.co/VHr8hn9/014-brain.png")
    await author.send(embed=embed)



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("Commande inconnue faites **/help**")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Il semblerait qu'un argument de la commande soit **incorrecte ou manquant faites /help**")

bot.run(os.getenv("TOKEN"))
